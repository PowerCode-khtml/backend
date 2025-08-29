import boto3
import os
import uuid
from fastapi import UploadFile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class S3Service:
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.upload_path = os.getenv("S3_UPLOAD_PATH")
        self.region_name = os.getenv("AWS_REGION",) # Use AWS_REGION from .env
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.s3 = boto3.client(
            "s3",
            region_name=self.region_name, # Use the region from .env
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def upload_file(self, file: UploadFile) -> str | None:
        """
        S3에 파일을 업로드하고 해당 URL을 반환합니다.
        """
        try:
            # 랜덤 파일명 생성
            file_extension = os.path.splitext(file.filename)[1]
            random_filename = f"{uuid.uuid4()}{file_extension}"
            s3_key = f"{self.upload_path}/{random_filename}"

            self.s3.upload_fileobj(
                file.file,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # S3 URL 구성 (리전별 엔드포인트 고려)
            # Use self.region_name here
            url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{s3_key}"
            return url
        except Exception as e:
            print(f"S3 업로드 오류: {e}")
            return None
