def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width, splitting on word boundaries.
    Preserves explicit line breaks (\n) as paragraph breaks."""
    lines = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        current_line = ""
        for word in words:
            test_line = word if not current_line else current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines
