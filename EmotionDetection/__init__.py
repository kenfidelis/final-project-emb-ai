"""
EmotionDetection Package

This package provides emotion detection functionality using IBM Watson NLP service.
It analyzes text and returns emotion scores for anger, disgust, fear, joy, and sadness,
along with the dominant emotion.
"""

from .emotion_detection import emotion_detector

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ["emotion_detector"]