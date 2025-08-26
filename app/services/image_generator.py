"""
AI 이미지 생성 서비스 (해커톤 특별 기능)
"""
from openai import OpenAI
import base64
import os
import uuid
from typing import Optional
import aiofiles

def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id
  
def encode_image(file_path):
    with open(file_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    return base64_image

class ImageGeneratorService:
    def __init__(self):
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 디렉토리 설정
        self.upload_dir = "/app/uploads"
        self.generated_dir = "/app/generated"
        
        # 디렉토리 생성
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
    
    def create_store_prompt(self, store_name: str, store_description: str, 
                           category: str, style: str = "modern") -> str:
        """상점 정보 기반 프롬프트 생성"""
        base_prompt = f"""Create an attractive poster for a {category} store named '{store_name}'.
        
Store Information:
- Name: {store_name}
- Category: {category}
- Description: {store_description}
- Style: {style}

Create a professional, eye-catching poster that would attract customers.
Make it suitable for social media and store promotion."""
        
        return base_prompt
    
    def create_product_prompt(self, product_name: str, product_description: str,
                            store_name: str, style: str = "modern") -> str:
        """상품 정보 기반 프롬프트 생성"""
        base_prompt = f"""Create an attractive product promotion poster.
        
Product Information:
- Product: {product_name}
- Description: {product_description}
- Store: {store_name}
- Style: {style}

Create a mouth-watering, appealing poster that showcases this product.
Make it perfect for social media marketing."""
        
        return base_prompt
    
    def create_event_prompt(self, event_name: str, event_description: str,
                          store_name: str, style: str = "modern") -> str:
        """이벤트 정보 기반 프롬프트 생성"""
        base_prompt = f"""Create an exciting event promotion poster.
        
Event Information:
- Event: {event_name}
- Description: {event_description}
- Store: {store_name}
- Style: {style}

Create an exciting, festive poster that promotes this event.
Make it engaging and shareable on social media."""
        
        return base_prompt
    
    async def generate_feed_image(self, prompt: str, image_file, feed_type: str = "store") -> dict:
        """
        피드용 이미지 생성 (해커톤 핵심 기능)
        """
        try:
            base64_image1 = encode_image(image_file)
            file_id = create_file(image_file)
            
            response = self.client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image1}",
                        },
                        {
                            "type": "input_image",
                            "file_id": file_id,
                        },
                      ],
                    }
                ],
                 tools=[{"type": "image_generation"}],
            )

            image_generation_calls = [
            output
            for output in response.output
            if output.type == "image_generation_call"
            ]

            image_data = [output.result for output in image_generation_calls]

            output_filename = f"{feed_type}_{uuid.uuid4()}.png"
            output_path = os.path.join(self.generated_dir, output_filename)

            if image_data:
                image_base64 = image_data[0]
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(image_base64))
            else:
                print(response.output.content)
            
            return {
                "success": True,
                "message": "이미지가 성공적으로 생성되었습니다",
                "filename": output_filename,
                "file_path": output_path,
                "mediaUrl": f"/generated/{output_filename}",
                "prompt_used": prompt
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"이미지 생성 중 오류 발생: {str(e)}",
                "error": str(e)
            }
    
    async def quick_store_poster(self, store_name: str, store_description: str,
                               category: str, message: str = "새로운 소식이 있어요!",
                               style: str = "modern") -> dict:
        """빠른 상점 포스터 생성 (해커톤용 간편 기능)"""
        
        prompt = f"""Create a quick promotional poster for '{store_name}' ({category}).
        
Message: {message}
Description: {store_description}
Style: {style}
        
Make it simple, clean and perfect for quick social media posting."""
        
        return await self.generate_feed_image(prompt, "quick_store")
