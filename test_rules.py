#!/usr/bin/env python3
"""
Test script for content moderation rules.
"""
from src.utils.rules import check_content_rules


def test_rules():
    """Test the content moderation rules."""
    
    print("Testing Content Moderation Rules\n")
    print("="*60)
    
    test_cases = [
        ("This is a great dress! Love it! #fashion", False),
        ("I want a refund for this terrible product", True),
        ("This is a scam! Never again!", True),
        ("Check out competitor1's new collection", True),
        ("We prefer using other brand for events", True),
        ("There's a lawsuit about this issue", True),
        ("Great event yesterday! Thanks everyone!", False),
        ("Disappointed with the service, need money back", True),
        ("Beautiful dress for the summer!", False),
        ("This is awful and I want a refund", True),
    ]
    
    passed = 0
    failed = 0
    
    for content, should_flag in test_cases:
        flagged, reason = check_content_rules(content)
        
        status = "✅ PASS" if flagged == should_flag else "❌ FAIL"
        if flagged == should_flag:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status}")
        print(f"Content: {content[:50]}...")
        print(f"Expected flagged: {should_flag}, Got: {flagged}")
        if flagged:
            print(f"Reason: {reason}")
    
    print("\n" + "="*60)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {failed} tests failed")


if __name__ == "__main__":
    test_rules()
