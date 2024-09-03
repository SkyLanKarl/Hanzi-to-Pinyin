import os
import re
from pypinyin import pinyin, Style
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def convert_to_pinyin(hanzi):
    # 将汉字转换为带声调的拼音
    pinyin_list = pinyin(hanzi, style=Style.TONE3)
    # 将拼音列表拼接成字符串，中间用连字符'-'分隔
    pinyin_str = '-'.join(word[0] for word in pinyin_list)
    return pinyin_str

def rename_files_in_directory(directory):
    renamed = False
    # 获取当前脚本的文件名
    current_script = os.path.basename(__file__)
    # 获取指定目录下的所有文件
    for filename in os.listdir(directory):
        # 跳过目录和当前脚本文件
        if os.path.isdir(os.path.join(directory, filename)) or filename == current_script:
            continue
        
         # 仅处理MP3文件
        if not filename.lower().endswith('.mp3'):
            continue

        # 将文件名分离为名称和扩展名
        name, ext = os.path.splitext(filename)
        
        # 提取文件名中的汉字部分
        chinese_part = re.sub(r'[^\u4e00-\u9fff]', '', name)
        
        if chinese_part:
            # 检查文件名是否已经包含拼音，避免重复添加
            pinyin_name = convert_to_pinyin(chinese_part)
            if pinyin_name not in name:
                # 将拼音附加到原文件名后面，但不重复添加英文部分
                new_name = f"{name}-{pinyin_name}{ext}"
            else:
                new_name = f"{name}{ext}"
                renamed = True
        else:
            new_name = f"{name}{ext}"
            
        
        # 生成新的文件路径
        new_filepath = os.path.join(directory, new_name)
        
        # 重命名文件
        old_filepath = os.path.join(directory, filename)
        os.rename(old_filepath, new_filepath)
        if renamed == False: 
            print(f'Renamed "{filename}" to "{new_name}"')
            print(f'重命名 "{filename}" 到 "{new_name}"')
        else:
            print("File name aleady renamed")
            print("拼音已加入")

        # 修改ID3标签
        audio = MP3(new_filepath, ID3=EasyID3)
        
        if chinese_part:
            # 更新 title 字段
            if 'title' in audio:
                title_name = audio['title'][0]
                title_chinese_part = re.sub(r'[^\u4e00-\u9fff]', '', title_name)
                title_pinyin = convert_to_pinyin(title_chinese_part)
                if title_chinese_part and title_pinyin not in title_name:
                    audio['title'] = f"{title_name}-{title_pinyin}"

            # 更新 artist 字段
            if 'artist' in audio:
                artist_name = audio['artist'][0]
                artist_chinese_part = re.sub(r'[^\u4e00-\u9fff]', '', artist_name)
                artist_pinyin = convert_to_pinyin(artist_chinese_part)
                if artist_chinese_part and artist_pinyin not in artist_name:
                    audio['artist'] = f"{artist_name}-{artist_pinyin}"

            # 更新 album 字段
            if 'album' in audio:
                album_name = audio['album'][0]
                album_chinese_part = re.sub(r'[^\u4e00-\u9fff]', '', album_name)
                album_pinyin = convert_to_pinyin(album_chinese_part)
                if album_chinese_part and album_pinyin not in album_name:
                    audio['album'] = f"{album_name}-{album_pinyin}"


        audio.save()


# 使用示例
current_directory = os.path.dirname(os.path.abspath(__file__))
rename_files_in_directory(current_directory)



