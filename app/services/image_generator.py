"""
AI 이미지 생성 서비스 (해커톤 특별 기능)
"""
from openai import OpenAI
import base64
import os
import uuid
from typing import Optional
import aiofiles
from fastapi import UploadFile

class ImageGeneratorService:
    def __init__(self):
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 디렉토리 설정
        self.upload_dir = "./uploads"
        self.generated_dir = "./generated"
        
        # 디렉토리 생성
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)

    def create_store_prompt(self, store_name: str, store_description: str) -> str:
        """Creates a promotional prompt for a store"""
        return f"Edit the provided image to create a promotional poster for a store named '{store_name}'. Store description: {store_description}. The poster should look professional, eye-catching, and be suitable for social media. The text on the poster must be in Korean."

    def create_product_prompt(self, product_name: str, product_description: str, store_name: str) -> str:
        """Creates a promotional prompt for a product"""
        return f"Edit the provided image to create a promotional poster for the product '{product_name}' from the store '{store_name}'. Product description: {product_description}. The poster should be attractive and suitable for social media marketing. The text on the poster must be in Korean."

    def create_event_prompt(self, event_name: str, event_description: str) -> str:
        """Creates a promotional prompt for an event"""
        return f"Edit the provided image to create a promotional poster for the event '{event_name}'. Event description: {event_description}. The poster should be interesting and shareable on social media. The text on the poster must be in Korean."

    async def save_uploaded_file(self, upload_file: UploadFile) -> str:
        """업로드된 파일을 임시 저장하고 경로를 반환"""
        temp_filename = f"{uuid.uuid4()}_{upload_file.filename}"
        temp_file_path = os.path.join(self.upload_dir, temp_filename)
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await upload_file.read()
            await out_file.write(content)
        return temp_file_path

    async def generate_image(self, prompt: str, upload_file: Optional[UploadFile] = None) -> dict:
        """
        gpt-4.1을 사용하여 프롬프트와 선택적 이미지를 기반으로 이미지를 생성합니다.
        """
        try:
            content = [{"type": "input_text", "text": prompt}]

            if upload_file:
                # 파일을 임시 저장하고 경로를 가져옵니다.
                temp_file_path = await self.save_uploaded_file(upload_file)

                # 이미지를 base64로 인코딩합니다.
                async with aiofiles.open(temp_file_path, "rb") as f:
                    base64_image = base64.b64encode(await f.read()).decode("utf-8")
                
                content.append({
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                })

                # The openai library's file upload is synchronous
                with open(temp_file_path, "rb") as file_content:
                    result = self.client.files.create(
                        file=file_content,
                        purpose="vision",
                    )
                
                file_id = result.id
                
                content.append({
                    "type": "input_image",
                    "file_id": file_id
                })

            response = self.client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                tools=[{"type": "image_generation"}],
            )

            image_generation_calls = [
                output
                for output in response.output
                if output.type == "image_generation_call"
            ]

            if not image_generation_calls:
                text_outputs = [
                    output.text
                    for output in response.output
                    if hasattr(output, 'text')
                ]
                error_message = text_outputs[0] if text_outputs else "Image generation failed for an unknown reason."
                print(f"Error during image generation: {error_message}")
                return {"success": False, "error": error_message}

            image_b64 = image_generation_calls[0].result
            
            output_filename = f"generated_{uuid.uuid4()}.png"
            output_path = os.path.join(self.generated_dir, output_filename)

            async with aiofiles.open(output_path, "wb") as f:
                await f.write(base64.b64decode(image_b64))

            return {
                "success": True,
                "mediaUrl": f"/home/teom142/goinfre/study/market/backend/generated/{output_filename}",
            }
        except Exception as e:
            print(f"Error during image generation: {e}")
            return {"success": False, "error": str(e)}