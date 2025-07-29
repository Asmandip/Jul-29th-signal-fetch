def ai_filter(signal_data, threshold=0.75):
    """
    Filters signal data based on AI confidence threshold.
    Args:
        signal_data (dict): Must contain a 'confidence' key with float value (0 to 1)
        threshold (float): Confidence threshold to allow signal
    Returns:
        bool: True if passes filter, False otherwise
    """
    confidence = signal_data.get('confidence', 0)
    return confidence >= threshold