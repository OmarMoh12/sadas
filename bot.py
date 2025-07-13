import os
#from ROQ9 import decode

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram import Update

import os
import json
import time
import secrets
import binascii
import string
import random
import uuid
from datetime import datetime, timedelta
from uuid import uuid4
from urllib.parse import urlencode
import os
import sys
import dis
import ast
import re
import zlib
import lzma
import base64 
import marshal
from py_compile import compile



# TOKEN BOT
TOKEN = ""

# BUILD BOT
bot = ApplicationBuilder().token(TOKEN).build()

class decode():


    def generate_pyc_file(file:str, output:str):
        extracted_objects = []
        with open(file, 'rb') as f:
            content = f.read()


        pattern = rb"'([^'\\]*(?:\\.[^'\\]*)*)'"

            
        matches = re.findall(pattern, content)

        for match in matches:
            byte_string = b"b'" + match + b"'"
            try:
                python_object = ast.literal_eval(byte_string.decode('utf-8')) 
                if isinstance(python_object, bytes):
                    extracted_objects.append(python_object)  
                else:
                    extracted_objects.append(python_object)  
            except Exception as e:
                return None
        extracted_data = extracted_objects


        for item in extracted_data:
            try:
                s = zlib.decompress(base64.b64decode(item))
            except:
                try:
                    s = zlib.decompress(base64.b64decode(item[::-1]))
                except:
                    try:
                        s = lzma.decompress(base64.b64decode(item))
                    except:
                        s = item


        with open(file, "w") as f:
            f.write(f'import marshal \nexec(marshal.loads({str(s)}))')
            try:
                try:
                    compile(file, cfile=file + 'c')
                    pyc = file + 'c'
                except Exception as e:
                    return None
                if pyc:
                    try:
                        with open(pyc, 'rb') as f:
                            magic_number = f.read(16)
                    except Exception as e:
                        os.remove(pyc)
                        return None
                    os.remove(pyc)
                else:
                    return None
            except Exception as e:
                return None

        if  not magic_number:
            return None
        
        marshal_c = marshal.loads(s)

        name, _ = os.path.splitext(file)

        with open(output, 'wb') as pyc:
            pyc.write(magic_number)

            marshal.dump(dis.Bytecode(marshal_c).codeobj, pyc)
            return output
            #result = os.popen(f'.\pycdas dec_{file}.pyc').read()
            #with open(f'dec_bytecode.py', 'w') as f:
            #    f.write(result)
            #marshal.dump(dis.Bytecode(result).codeobj, pyc)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""✨ أهلاً بك في بوت فك تشفير بايثون! ✨

أرسل لي ملف py وسأقوم بتحويله إلى ملف pyc جاهز لفك التشفير. 😉
    """
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""📚 **تعليمات استخدام البوت** 📚

1.  أرسل لي ملف بايثون المراد تحويله الى pyc  . 📎
2.  سأقوم تلقائيًا بتحويل الملف إلى ملف  (.pyc) وإرساله إليك. ✅
3.  يمكنك استخدام الأمر /start لعرض رسالة الترحيب والأمر /help لعرض هذه التعليمات.
    """
    )


async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    try:
        file_id = update.message.document.file_id
        file_unique_id = update.message.document.file_unique_id
        file_name = update.message.document.file_name
        name, _ = os.path.splitext(file_name)

        await context.bot.send_message(
            chat_id=chat_id, text="⏳ جاري فك تشفير الملف، يرجى الانتظار... ⏳"
        )

        temp_file = await context.bot.get_file(file_id)
        await temp_file.download_to_drive(f'./temp/{file_unique_id}.py')

        process = decode.generate_pyc_file(f'./temp/{file_unique_id}.py', f'./processed/{name}.pyc')
        os.remove(f'./temp/{file_unique_id}.py')

        if process is None:
            await context.bot.send_message(chat_id=chat_id, text="❌ حدث خطأ أثناء فك التشفير. ❌")
        else:
            await context.bot.send_document(
                chat_id=chat_id, document=f'./processed/{name}.pyc',
                caption="✅ تم تحويل بنجاح! ✅"
            )
            print("✅ تم تحويل بنجاح! ✅")
            os.remove(f'./processed/{name}.pyc')

    except Exception as e:
        print(f"Error: {e}")
        os.remove(f'./temp/{file_unique_id}.py')
        await context.bot.send_message(chat_id=chat_id, text="❌ حدث خطأ غير متوقع. ❌")


#Handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
file_handler = MessageHandler(filters.Document.ALL, process_file)

# إضافة المعالجات
bot.add_handler(start_handler)
bot.add_handler(help_handler)
bot.add_handler(file_handler)

if __name__ == '__main__':
    print("البوت يعمل الآن! 🚀")
    bot.run_polling()
    