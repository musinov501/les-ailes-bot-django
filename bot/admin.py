import asyncio
import os

from aiogram.types import BufferedInputFile
from django.contrib import admin

from bot.apps import BotConfig
from bot.models.base import City
from bot.models.product import Product, Category
from core import config


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption_short', 'created_at']
    list_filter = ['created_at']
    search_fields = ['caption', 'file_id']
    readonly_fields = ['file_id', 'file_unique_id', 'created_at']

    def caption_short(self, obj):
        """Show truncated caption in list view"""
        if obj.caption:
            return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
        return '-'

    caption_short.short_description = "Caption"

    def save_model(self, request, obj, form, change):
        """Upload image to Telegram before saving"""
        if obj.temp_file and not obj.file_id:
            try:
                # Upload to Telegram and get file_id
                file_id, file_unique_id = self._upload_to_telegram(obj.temp_file, obj.caption)

                # Check if this image already exists
                existing = Product.objects.filter(file_unique_id=file_unique_id).first()
                if existing:
                    # Clean up temp file
                    obj.temp_file.delete(save=False)

                    self.message_user(
                        request,
                        f"This image already exists in the database (ID: {existing.id}). "
                        f"Telegram file_unique_id: {file_unique_id}. "
                        f"You can reuse the existing file_id: {existing.file_id}",
                        level='WARNING'
                    )
                    # Don't save the duplicate
                    return

                obj.file_id = file_id
                obj.file_unique_id = file_unique_id

                # Save the object
                super().save_model(request, obj, form, change)

                # Clean up temp file
                if obj.temp_file:
                    obj.temp_file.delete(save=False)

                self.message_user(
                    request,
                    f"✅ Image uploaded to Telegram successfully! File ID: {file_id}",
                    level='SUCCESS'
                )

            except Exception as e:
                # Clean up temp file
                if obj.temp_file:
                    obj.temp_file.delete(save=False)

                self.message_user(
                    request,
                    f"❌ Error uploading to Telegram: {str(e)}",
                    level='ERROR'
                )
                raise
        else:
            super().save_model(request, obj, form, change)

    def _upload_to_telegram(self, file_field, caption=None):

        storage_chat_id = getattr(config, 'TELEGRAM_STORAGE_CHAT_ID', None)

        if not storage_chat_id:
            raise ValueError(
                "TELEGRAM_STORAGE_CHAT_ID not set in settings. "
                "Please add your Telegram user ID or channel ID to settings.py"
            )

        # Read file content
        file_field.seek(0)
        file_content = file_field.read()
        file_name = os.path.basename(file_field.name)

        # Create BufferedInputFile
        input_file = BufferedInputFile(
            file=file_content,
            filename=file_name
        )

        # Running async task safely
        result = asyncio.run(
            self._send_to_telegram(
                BotConfig.bot,
                storage_chat_id,
                input_file,
                caption
            )
        )

        return result["file_id"], result["file_unique_id"]


    @staticmethod
    async def _send_to_telegram(bot, chat_id, input_file, caption):
        message = await bot.send_photo(
            chat_id=chat_id,
            photo=input_file,
            caption=caption
        )

        if not message.photo:
            raise ValueError("Telegram did not return a photo. Probably file is not an image.")

        return {
            "file_id": message.photo[-1].file_id,
            "file_unique_id": message.photo[-1].file_unique_id
        }



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']


@admin.register(City)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']