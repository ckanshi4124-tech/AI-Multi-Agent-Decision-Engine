import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Lightweight rule-based sentiment analyzer optimized for
    low-memory cloud deployment environments.
    """

    def __init__(self):
        logger.info("Lightweight sentiment analyzer initialized")

        self.positive_words = {
            "growth", "profit", "success", "strong", "scaling",
            "improving", "excellent", "expansion", "demand",
            "increase", "positive", "bullish", "opportunity",
            "good", "favorable", "efficient", "innovative",
            "stable", "robust", "promising"
        }

        self.negative_words = {
            "loss", "decline", "drop", "churn", "weak",
            "poor", "crash", "issue", "problem", "decreasing",
            "negative", "bearish", "risk", "threat",
            "uncertain", "downturn", "failure", "unstable",
            "delay", "challenge"
        }

        self.mixed_indicators = {
            "but", "however", "although", "though",
            "yet", "nevertheless"
        }

    def analyze(self, text: str):
        """
        Analyze sentiment and return:
        {
            "label": "Positive|Negative|Neutral",
            "confidence": float,
            "reason": str
        }
        """
        try:
            # ---------------------------
            # Input Validation
            # ---------------------------
            if not text or not isinstance(text, str) or not text.strip():
                return {
                    "label": "Neutral",
                    "confidence": 0.5,
                    "reason": "Empty or invalid text"
                }

            text_clean = text.strip()
            text_lower = text_clean.lower()
            words = set(text_lower.split())

            # ---------------------------
            # Base Counts
            # ---------------------------
            positive_hits = len(words & self.positive_words)
            negative_hits = len(words & self.negative_words)

            reasons = []

            # ---------------------------
            # Initial Classification
            # ---------------------------
            if positive_hits > negative_hits:
                label = "Positive"
                confidence = 0.65 + (0.03 * positive_hits)
                reasons.append(
                    f"Detected {positive_hits} positive keyword(s)"
                )

            elif negative_hits > positive_hits:
                label = "Negative"
                confidence = 0.65 + (0.03 * negative_hits)
                reasons.append(
                    f"Detected {negative_hits} negative keyword(s)"
                )

            else:
                label = "Neutral"
                confidence = 0.50
                reasons.append("Balanced or no sentiment keywords")

            # ---------------------------
            # Mixed Sentiment Adjustment
            # ---------------------------
            if any(indicator in text_lower for indicator in self.mixed_indicators):
                confidence -= 0.05
                reasons.append("Mixed sentiment indicator detected")

            # ---------------------------
            # Normalize Confidence
            # ---------------------------
            confidence = round(
                max(0.0, min(0.95, confidence)),
                2
            )

            return {
                "label": label,
                "confidence": confidence,
                "reason": "; ".join(reasons)
            }

        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")

            return {
                "label": "Neutral",
                "confidence": 0.5,
                "reason": "Error fallback"
            }


# Singleton instance
analyzer = SentimentAnalyzer()


def sentiment_analyze(text: str):
    """
    Convenience wrapper used by other modules.
    """
    return analyzer.analyze(text)
    