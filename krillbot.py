from aiogram import Bot,Dispatcher,types,F
import asyncio
from aiogram.filters import Command
from anaylise import has_cyrillic
from baza import to_cyrillic,to_latin
from read_word import word_reader
tokenAPI='6960765694:AAFvV8bhNpELWoWAkxeO4QaKn8ZFnm1x9XY'
bot=Bot(token=tokenAPI,parse_mode='HTML')
dp=Dispatcher()

@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer('Welcome')

@dp.message(F.text)
async def get_photo(message:types.Message):
    txt=message.text
    if has_cyrillic(text=txt):
        await message.answer(to_latin(txt))
    else:
        await message.answer(to_cyrillic(txt))
@dp.message(F.document)
async def get_doc(message:types.Message):
    doc=message.document
    file_id=doc.file_id
    file_name=str(doc.file_name)
    document_type=file_name[file_name.rindex('.')+1:]
    if document_type=='docx':
        file=await bot.get_file(file_id=file_id)
        custom_file=f'{doc.file_unique_id}.docx'
        await bot.download(file=file,destination=custom_file)
        data=await message.answer('Fayl yuklandi')
        green='🟩'
        white='⬜️'
        for i in range(1,11):
            percent=i*10
            await data.edit_text(f'Fayl jarayonda... \n'\
                                 f'{i*green}{(10-i)*white}\n'\
                                 f'Downloading {percent}% 100')
        await data.delete()
        word_reader(custom_file)
        new_doc=types.input_file.FSInputFile(path=custom_file,filename=file_name)
        await message.answer_document(document=new_doc,caption='Converted document')
        try:
            import os
            if os.path.isfile(custom_file):
                os.remove(custom_file)
        except:
            pass

async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())
