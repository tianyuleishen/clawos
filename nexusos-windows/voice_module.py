#!/usr/bin/env python3
"""
🦞 NexusOS 语音合成模块
独立运行，不依赖大模型
支持多种音色选择
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime
from typing import Optional, Dict

class NexusOSVoice:
    """NexusOS语音系统"""
    
    # 音色配置
    VOICES = {
        "xiaozhua": {
            "name": "小爪",
            "speed": 1.0,
            "pitch": 1.0,
            "description": "温暖活泼的青年音"
        },
        "professional": {
            "name": "专业播音",
            "speed": 0.9,
            "pitch": 1.0,
            "description": "沉稳专业的播音腔"
        },
        "friendly": {
            "name": " friendly",
            "speed": 1.1,
            "pitch": 1.1,
            "description": "亲切友好的声音"
        },
        "energetic": {
            "name": "活力",
            "speed": 1.2,
            "pitch": 1.1,
            "description": "充满活力的声音"
        },
        "calm": {
            "name": "平静",
            "speed": 0.85,
            "pitch": 0.95,
            "description": "平静温和的声音"
        }
    }
    
    def __init__(self, default_voice: str = "xiaozhua"):
        self.default_voice = default_voice
        self.output_dir = "/tmp/nexusos_voice"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 尝试导入TTS库
        self.gtts_available = False
        self.pyttsx3_available = False
        
        try:
            from gtts import gTTS
            self.gtts_available = True
            print("✅ gTTS语音库可用")
        except ImportError:
            print("⚠️ gTTS未安装，将使用备用方案")
        
        try:
            import pyttsx3
            self.pyttsx3_available = True
            self.engine = pyttsx3.init()
            # 设置默认参数
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            print("✅ pyttsx3语音引擎可用")
        except ImportError:
            print("⚠️ pyttsx3未安装")
        
        print(f"\n{'='*70}")
        print(f"🔊 NexusOS 语音系统就绪")
        print(f"   默认音色: {self.VOICES[default_voice]['name']}")
        print(f"   gTTS: {'✅' if self.gtts_available else '❌'}")
        print(f"   pyttsx3: {'✅' if self.pyttsx3_available else '❌'}")
        print(f"{'='*70}")
    
    def speak(self, text: str, voice: str = None, save: bool = True) -> Optional[str]:
        """
        文字转语音
        
        Args:
            text: 要转换的文字
            voice: 音色选择
            save: 是否保存音频文件
        
        Returns:
            音频文件路径 或 None
        """
        voice = voice or self.default_voice
        voice_config = self.VOICES.get(voice, self.VOICES["xiaozhua"])
        
        print(f"\n🔊 语音合成: {text[:30]}...")
        print(f"   音色: {voice_config['name']}")
        
        # 方法1: 使用pyttsx3 (离线首选)
        if self.pyttsx3_available:
            return self._speak_pyttsx3(text, voice_config, save)
        
        # 方法2: 使用gTTS (在线)
        elif self.gtts_available:
            return self._speak_gtts(text, voice_config, save)
        
        # 方法3: 使用Web TTS API
        else:
            return self._speak_webapi(text, voice_config, save)
    
    def _speak_pyttsx3(self, text: str, voice_config: Dict, save: bool = True) -> Optional[str]:
        """使用pyttsx3 (离线)"""
        try:
            # 设置语速
            rate = int(150 * voice_config['speed'])
            self.engine.setProperty('rate', rate)
            
            # 设置音量
            self.engine.setProperty('volume', 1.0)
            
            # 保存到文件
            if save:
                filename = f"{self.output_dir}/nexusos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                self.engine.save_to_file(text, filename)
                self.engine.runAndWait()
                print(f"   ✅ 已保存: {filename}")
                return filename
            else:
                self.engine.say(text)
                self.engine.runAndWait()
                return None
                
        except Exception as e:
            print(f"   ❌ pyttsx3错误: {e}")
            return None
    
    def _speak_gtts(self, text: str, voice_config: Dict, save: bool = True) -> Optional[str]:
        """使用gTTS (在线)"""
        try:
            from gtts import gTTS
            
            # 调整语速
            slow = voice_config['speed'] < 1.0
            
            tts = gTTS(text=text, lang='zh-cn', slow=slow)
            
            if save:
                filename = f"{self.output_dir}/nexusos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                tts.save(filename)
                print(f"   ✅ 已保存: {filename}")
                return filename
            else:
                # 直接播放
                tts.write_to_fp(open('/dev/null', 'wb'))
                return None
                
        except Exception as e:
            print(f"   ❌ gTTS错误: {e}")
            return None
    
    def _speak_webapi(self, text: str, voice_config: Dict, save: bool = True) -> Optional[str]:
        """使用Web TTS API"""
        try:
            # 使用免费的TTS API
            url = "https://tts.baidu.com/text2audio"
            
            params = {
                "tex": text,
                "per": 0,  # 百度语音员
                "spd": int(5 * voice_config['speed']),
                "vol": 5,
                "pit": int(5 * voice_config['pitch']),
                "aue": 3,
                "cuid": "nexusos001",
                "lan": "zh",
                "ctp": 1,
                "res_id": "rest"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200 and len(response.content) > 1000:
                if save:
                    filename = f"{self.output_dir}/nexusos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"   ✅ 已保存: {filename}")
                    return filename
                else:
                    print("   ✅ 语音合成成功")
                    return None
            else:
                print(f"   ❌ API返回错误")
                return None
                
        except Exception as e:
            print(f"   ❌ Web TTS错误: {e}")
            return None
    
    def play_audio(self, filename: str):
        """播放音频"""
        if not os.path.exists(filename):
            print(f"❌ 文件不存在: {filename}")
            return
        
        # 根据系统选择播放方式
        if sys.platform == "win32":
            os.startfile(filename)
        elif sys.platform == "darwin":
            os.system(f"afplay {filename}")
        else:
            # Linux
            players = ["aplay", "paplay", "mpg123", "play"]
            for player in players:
                if os.system(f"which {player} > /dev/null 2>&1") == 0:
                    os.system(f"{player} {filename}")
                    break
    
    def list_voices(self):
        """列出可用音色"""
        print("\n🎭 可用音色:")
        for key, voice in self.VOICES.items():
            marker = "←" if key == self.default_voice else " "
            print(f"   {marker} {key}: {voice['name']} ({voice['description']})")
    
    def set_default_voice(self, voice: str):
        """设置默认音色"""
        if voice in self.VOICES:
            self.default_voice = voice
            print(f"✅ 默认音色已设置为: {self.VOICES[voice]['name']}")
        else:
            print(f"❌ 未知的音色: {voice}")


class VoiceAssistant:
    """语音助手 - 整合语音交互"""
    
    def __init__(self):
        self.voice = NexusOSVoice()
        self.listen_enabled = False
        self.stt_available = False
        
        # 尝试导入语音识别
        try:
            import speech_recognition
            self.stt_available = True
            self.recognizer = speech_recognition.Recognizer()
            print("✅ 语音识别可用")
        except ImportError:
            print("⚠️ 语音识别未安装")
    
    def listen(self) -> Optional[str]:
        """语音输入 (需要麦克风)"""
        if not self.stt_available:
            print("❌ 语音识别未安装")
            return None
        
        try:
            with speech_recognition.Microphone() as source:
                print("🎤  listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            # 识别 (使用Google免费API)
            text = self.recognizer.recognize_google(audio, language='zh-CN')
            print(f"📝 识别结果: {text}")
            return text
            
        except speech_recognition.WaitTimeoutError:
            print("⏱️ 等待超时")
            return None
        except Exception as e:
            print(f"❌ 识别错误: {e}")
            return None
    
    def say_and_listen(self, prompt: str = "请说话") -> Optional[str]:
        """说并听"""
        self.voice.speak(prompt)
        return self.listen()


# ========== 测试 ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 测试NexusOS语音系统")
    print("="*70)
    
    # 创建语音系统
    voice = NexusOSVoice()
    
    # 列出音色
    voice.list_voices()
    
    # 测试语音合成
    print("\n🔊 测试语音合成:")
    test_text = "你好！我是NexusOS语音助手"
    
    # 测试不同音色
    for v in ["xiaozhua", "professional", "friendly"]:
        print(f"\n🎭 音色: {v}")
        voice.speak(test_text, voice=v)
    
    print("\n" + "="*70)
    print("✅ 语音系统测试完成!")
    print("="*70)
