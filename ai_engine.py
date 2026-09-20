from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

print("Loading AI model...")

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

print("AI model loaded!")


def analyze_image(image):

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=50
        )

    description = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    description = description.strip()

    # Simple civic issue detection
    text = description.lower()

    if "pothole" in text or "hole" in text:
        issue = "🕳️ Pothole"

    elif "garbage" in text or "trash" in text or "rubbish" in text:
        issue = "🗑️ Garbage"

    elif "tree" in text or "branch" in text:
        issue = "🌳 Fallen Tree"

    elif "light" in text or "lamp" in text:
        issue = "💡 Streetlight"

    elif "road" in text:
        issue = "🛣️ Road Problem"

    else:
        issue = "❓ Other Civic Issue"

    return issue, description