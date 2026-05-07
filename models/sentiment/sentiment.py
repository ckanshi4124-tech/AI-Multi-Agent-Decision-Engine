from transformers import pipeline
import logging


logger = logging.getLogger(__name__)


class SentimentAnalyzer:

    def __init__(self):

        self.model = None

        try:

            self.model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )

            logger.info("Sentiment model loaded")

        except Exception as e:

            logger.error(f"Model loading failed: {e}")

            self.model = None

    def analyze(self, text: str):

        try:

            # =========================
            # INPUT VALIDATION
            # =========================

            if not text or text.strip() == "":

                return {
                    "label": "Neutral",
                    "confidence": 0.5,
                    "reason": "Empty or invalid text"
                }

            text_clean = text.strip()

            label = "Neutral"

            confidence = 0.5

            reasons = []

            # =========================
            # MODEL PREDICTION
            # =========================

            if self.model:

                result = self.model(text_clean)[0]

                raw_label = result["label"]

                raw_score = float(
                    result["score"]
                )

                if raw_label.upper() == "POSITIVE":

                    label = "Positive"

                else:

                    label = "Negative"

                confidence = raw_score

                reasons.append(
                    f"Model detected {label.lower()} sentiment"
                )

            else:

                reasons.append(
                    "Fallback mode (model unavailable)"
                )

            # =========================
            # KEYWORD SUPPORT
            # =========================

            text_lower = text_clean.lower()

            positive_words = [

                "growth",
                "profit",
                "success",
                "strong",
                "scaling",
                "improving",
                "excellent",
                "expansion",
                "high demand"
            ]

            negative_words = [

                "loss",
                "decline",
                "drop",
                "churn",
                "weak",
                "poor",
                "crash",
                "issue",
                "problem",
                "decreasing"
            ]

            pos_hits = sum(
                1 for word in positive_words
                if word in text_lower
            )

            neg_hits = sum(
                1 for word in negative_words
                if word in text_lower
            )

            # Small adjustment only

            if pos_hits > neg_hits:

                confidence += 0.03

                reasons.append(
                    "Positive keywords detected"
                )

            elif neg_hits > pos_hits:

                confidence += 0.03

                reasons.append(
                    "Negative keywords detected"
                )

            # =========================
            # NEUTRAL DETECTION
            # =========================

            if 0.45 <= confidence <= 0.55:

                label = "Neutral"

                reasons.append(
                    "Low confidence → Neutral classification"
                )

            # =========================
            # MIXED SENTIMENT
            # =========================

            if any(
                word in text_lower
                for word in [
                    "but",
                    "however",
                    "although"
                ]
            ):

                confidence -= 0.05

                reasons.append(
                    "Mixed sentiment detected"
                )

            # =========================
            # FINAL NORMALIZATION
            # =========================

            confidence = round(

                max(
                    0.0,
                    min(0.99, confidence)
                ),

                2
            )

            return {

                "label": label,

                "confidence": confidence,

                "reason": ", ".join(reasons)
            }

        except Exception as e:

            logger.error(f"Sentiment error: {e}")

            return {

                "label": "Neutral",

                "confidence": 0.5,

                "reason": "Error fallback"
            }


# =========================
# SINGLETON
# =========================

analyzer = SentimentAnalyzer()


def sentiment_analyze(text: str):

    return analyzer.analyze(text)