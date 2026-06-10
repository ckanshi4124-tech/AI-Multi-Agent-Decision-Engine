import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Lightweight rule-based sentiment analyzer optimized for
    low-memory cloud deployment environments.
    """

    def __init__(self):
        logger.info("Initializing DistilBERT sentiment analyzer")

        from transformers import pipeline

        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

        logger.info("DistilBERT sentiment analyzer loaded")

    def analyze(self, text: str):
        try:

            if not text or not isinstance(text, str) or not text.strip():
                return {
                    "label": "Neutral",
                    "confidence": 0.5,
                    "reason": "Empty or invalid text"
                }

            result = self.classifier(text)[0]

            label = result["label"].upper()
            score = float(result["score"])

            if label == "POSITIVE":
                final_label = "Positive"

            elif label == "NEGATIVE":
                final_label = "Negative"

            else:
                final_label = "Neutral"

            return {
                "label": final_label,
                "confidence": round(score, 2),
                "reason": f"DistilBERT sentiment classification ({label})"
            }

        except Exception as e:

            logger.error(
                f"Sentiment analysis error: {e}"
            )

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
    