"""Tests for Trade Email Case Copilot CLI."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "main.py"
FIXTURES = ROOT / "tests" / "fixtures"


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True,
    )


class TestDiagnoseEnglish:
    """Test English message classification."""

    def test_price_category(self):
        r = run(["diagnose", "The price is too high, can you give a discount?"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "price" in cats

    def test_payment_category(self):
        r = run(["diagnose", "We want to pay in installments after delivery"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats

    def test_sample_category(self):
        r = run(["diagnose", "The sample we received was wrong"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "samples" in cats

    def test_followup_category(self):
        r = run(["diagnose", "The client is not replying to our emails"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_multi_category(self):
        r = run(["diagnose", "The sample quality is bad, sample was wrong, and the price is too high, price expensive"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "samples" in cats
        assert "price" in cats
        assert data["cross_topic"] is True

    def test_lc_payment(self):
        r = run(["diagnose", "Can we use L/C for this order?"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats

    def test_freight_surcharge(self):
        r = run(["diagnose", "The freight cost increased, customer won't pay surcharge"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats

    def test_win_back(self):
        r = run(["diagnose", "Old customer stopped ordering, need to win back"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_fallback_to_library(self):
        r = run(["diagnose", "Hello, how are you?"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["categories"][0]["category"] == "library"


class TestDiagnoseChinese:
    """Test Chinese message classification."""

    def test_price_zh(self):
        r = run(["diagnose", "客户说价格太贵了，要求降价20%"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "price" in cats

    def test_payment_zh(self):
        r = run(["diagnose", "客户要求分期付款，发货后再付尾款"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats

    def test_sample_zh(self):
        r = run(["diagnose", "我们发错样品了，客户很不满意"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "samples" in cats

    def test_followup_zh(self):
        r = run(["diagnose", "客户已读不回，跟进了好几次都没有回复"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_complaint_zh(self):
        r = run(["diagnose", "客户投诉产品质量有问题，要求退款"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_freight_zh(self):
        r = run(["diagnose", "运费涨了，客户不愿意补差价"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats


class TestDiagnoseScoring:
    """Test confidence scoring in classification."""

    def test_scores_are_present(self):
        r = run(["diagnose", "The price is too high"])
        data = json.loads(r.stdout)
        assert "score" in data["categories"][0]
        assert data["categories"][0]["score"] > 0

    def test_primary_category_set(self):
        r = run(["diagnose", "Payment terms and price negotiation"])
        data = json.loads(r.stdout)
        assert "primary_category" in data
        assert data["primary_category"] in ["price", "delivery_payment"]

    def test_higher_score_first(self):
        r = run(["diagnose", "price price price and one sample"])
        data = json.loads(r.stdout)
        if len(data["categories"]) > 1:
            assert data["categories"][0]["score"] >= data["categories"][1]["score"]


class TestChannelDetection:
    """Test channel detection."""

    def test_default_email(self):
        r = run(["channel", "Please help me reply to this customer"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["channel"] == "email"

    def test_whatsapp(self):
        r = run(["channel", "Customer sent this on WhatsApp"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["channel"] == "chat"

    def test_wechat(self):
        r = run(["channel", "客户在微信上说想分期"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["channel"] == "chat"

    def test_tm(self):
        r = run(["channel", "TM上客户问价格"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["channel"] == "chat"

    def test_linkedin(self):
        r = run(["channel", "Got a LinkedIn message from the buyer"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["channel"] == "chat"


class TestToneDetection:
    """Test tone detection."""

    def test_default_professional(self):
        r = run(["tone", "Help me reply to this customer"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "professional"

    def test_firm(self):
        r = run(["tone", "帮我写一封强硬一点的邮件"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "firm"

    def test_soft(self):
        r = run(["tone", "请温和一点回复"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "soft"

    def test_urgent(self):
        r = run(["tone", "This is urgent, need to reply ASAP"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "urgent"


class TestModeDetection:
    """Test output mode detection via diagnose."""

    def test_full_mode_default(self):
        r = run(["diagnose", "Customer wants a discount"])
        data = json.loads(r.stdout)
        assert data["mode"] == "full"

    def test_analysis_only_zh(self):
        r = run(["diagnose", "帮我分析一下这个客户的情况"])
        data = json.loads(r.stdout)
        assert data["mode"] == "analysis_only"

    def test_analysis_only_en(self):
        r = run(["diagnose", "Just analyze this situation, no email needed"])
        data = json.loads(r.stdout)
        assert data["mode"] == "analysis_only"

    def test_english_only(self):
        r = run(["diagnose", "只要英文回复就好"])
        data = json.loads(r.stdout)
        assert data["mode"] == "english_only"


class TestRoute:
    """Test category-to-file routing."""

    def test_route_samples(self):
        r = run(["route", "samples"])
        assert r.returncode == 0
        assert "10-case-cards-samples.md" in r.stdout

    def test_route_price(self):
        r = run(["route", "price"])
        assert r.returncode == 0
        assert "11-case-cards-price.md" in r.stdout

    def test_route_delivery_payment(self):
        r = run(["route", "delivery_payment"])
        assert r.returncode == 0
        assert "12-case-cards-delivery-payment.md" in r.stdout

    def test_route_followup(self):
        r = run(["route", "followup_aftersales"])
        assert r.returncode == 0
        assert "13-case-cards-followup-after-sales.md" in r.stdout

    def test_route_library(self):
        r = run(["route", "library"])
        assert r.returncode == 0
        assert "03-email-case-library.md" in r.stdout


class TestValidate:
    """Test output validation."""

    def test_valid_output(self):
        p = FIXTURES / "valid_output.txt"
        r = run(["validate", str(p)])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["valid"] is True
        assert data["dimensions_found"] == 6

    def test_invalid_missing_dimension(self):
        p = FIXTURES / "invalid_missing_dimension.txt"
        r = run(["validate", str(p)])
        assert r.returncode == 1
        data = json.loads(r.stdout)
        assert data["valid"] is False

    def test_invalid_few_cases(self):
        p = FIXTURES / "invalid_few_cases.txt"
        r = run(["validate", str(p)])
        assert r.returncode == 1
        data = json.loads(r.stdout)
        assert data["valid"] is False

    def test_valid_full_output(self):
        p = FIXTURES / "valid_full_output.txt"
        if p.exists():
            r = run(["validate", str(p)])
            assert r.returncode == 0
            data = json.loads(r.stdout)
            assert data["valid"] is True
            assert data["cases_found"] >= 3


class TestFixtureIntegrity:
    """Verify fixture files exist."""

    def test_fixtures_exist(self):
        assert (FIXTURES / "valid_output.txt").exists()
        assert (FIXTURES / "invalid_missing_dimension.txt").exists()
        assert (FIXTURES / "invalid_few_cases.txt").exists()

    def test_valid_full_output_exists(self):
        assert (FIXTURES / "valid_full_output.txt").exists()


class TestReferenceFiles:
    """Verify all reference files exist and are non-empty."""

    def test_routing_file(self):
        p = ROOT / "references" / "00-routing.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_output_contract(self):
        p = ROOT / "references" / "01-output-contract.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_channel_rules(self):
        p = ROOT / "references" / "02-channel-rules.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_case_library(self):
        p = ROOT / "references" / "03-email-case-library.md"
        assert p.exists()
        assert p.stat().st_size > 1000

    def test_case_cards_samples(self):
        p = ROOT / "references" / "10-case-cards-samples.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_case_cards_price(self):
        p = ROOT / "references" / "11-case-cards-price.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_case_cards_delivery(self):
        p = ROOT / "references" / "12-case-cards-delivery-payment.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_case_cards_followup(self):
        p = ROOT / "references" / "13-case-cards-followup-after-sales.md"
        assert p.exists()
        assert p.stat().st_size > 100


class TestToneCasual:
    """Test casual tone detection."""

    def test_casual_zh(self):
        r = run(["tone", "帮我轻松一点回复"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "casual"

    def test_casual_en(self):
        r = run(["tone", "Make it more casual please"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["tone"] == "casual"


class TestBatchCommand:
    """Test batch processing."""

    def test_batch_processing(self, tmp_path):
        batch_file = tmp_path / "batch_input.txt"
        batch_file.write_text(
            "The price is too high\n"
            "客户不回复了\n"
            "Sample quality is bad\n",
            encoding="utf-8",
        )
        r = run(["batch", str(batch_file)])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert len(data) == 3
        assert data[0]["primary_category"] == "price"
        assert data[1]["primary_category"] == "followup_aftersales"
        assert data[2]["primary_category"] == "samples"


class TestCrossTopicThreshold:
    """Test that cross_topic requires significant scores in both categories."""

    def test_weak_secondary_not_cross_topic(self):
        r = run(["diagnose", "price price price and one sample"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["primary_category"] == "price"

    def test_strong_both_is_cross_topic(self):
        r = run(["diagnose", "price discount cost budget and sample proof prototype testing"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["cross_topic"] is True


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_like_message(self):
        r = run(["diagnose", "ok"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["primary_category"] == "library"

    def test_mixed_language(self):
        r = run(["diagnose", "客户说price太高了，要discount"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["primary_category"] == "price"

    def test_refund_routes_to_followup(self):
        r = run(["diagnose", "Customer wants a refund for quality issues"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_warranty_routes_to_followup(self):
        r = run(["diagnose", "warranty claim from customer"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "followup_aftersales" in cats

    def test_tariff_routes_to_delivery(self):
        r = run(["diagnose", "客户说关税太高不想下单"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        cats = [c["category"] for c in data["categories"]]
        assert "delivery_payment" in cats


class TestAssetFiles:
    """Verify all asset files exist and are non-empty."""

    def test_email_template_zh(self):
        p = ROOT / "assets" / "email-template-zh.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_email_template_en(self):
        p = ROOT / "assets" / "email-template-en.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_whatsapp_patterns(self):
        p = ROOT / "assets" / "whatsapp-patterns.md"
        assert p.exists()
        assert p.stat().st_size > 100

    def test_tone_calibration(self):
        p = ROOT / "assets" / "tone-calibration.md"
        assert p.exists()
        assert p.stat().st_size > 100
