from PIL import Image
import io

def preprocess_image(image_data):
    """Mock de preprocesamiento básico de imágenes"""
    try:
        img = Image.open(io.BytesIO(image_data))
        # Simular redimensionamiento y conversión de formato
        return img.convert('RGB').resize((224, 224))
    except Exception as e:
        raise ValueError(f"Error en preprocesamiento: {str(e)}")