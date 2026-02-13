# 🦞 Text-to-Speech - 语音合成

"""
语音合成 - 多引擎文字转语音

功能:
- 多引擎支持 (Edge TTS, Azure, 阿里云, etc.)
- 中文语音
- 多种声音
- 语速/音调控制
"""

import asyncio
import subprocess
import platform
from typing import Optional, AsyncIterator, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import base64
import io

class TTSEngine(Enum):
    """语音合成引擎"""
    EDGE = "edge"       # Microsoft Edge TTS (免费)
    AZURE = "azure"    # Azure Speech
    ALIYUN = "aliyun"  # 阿里云
    BAIDU = "baidu"    # 百度语音
    GOOGLE = "google"  # Google TTS
    ESPEAK = "espeak"  # eSpeak (免费)
    SAY = "say"        # macOS say
    COQUI = "coqui"    # Coqui TTS (本地)
    DEFAULT = "default"

@dataclass
class VoiceInfo:
    """语音信息"""
    id: str
    name: str
    gender: str
    language: str
    engine: str
    quality: str  # low, medium, high

@dataclass
class TTSResult:
    """语音合成结果"""
    text: str
    audio_data: bytes
    duration: float
    format: str
    engine: str
    voice_id: str
    success: bool
    error: str = None


class TextToSpeech:
    """语音合成器"""
    
    def __init__(self):
        self.platform = platform.system()
        self.default_voice = None
        print(f"✅ Text-to-Speech 已加载 ({self.platform})")
    
    # ============ 引擎检测 ============
    
    def detect_engine(self) -> TTSEngine:
        """检测可用的TTS引擎"""
        # 检查Edge TTS
        try:
            result = subprocess.run(
                ['pip', 'show', 'edge-tts'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return TTSEngine.EDGE
        except:
            pass
        
        # macOS say
        if self.platform == "Darwin":
            return TTSEngine.SAY
        
        # Linux espeak
        try:
            subprocess.run(['which', 'espeak'], capture_output=True)
            return TTSEngine.ESPEAK
        except:
            pass
        
        return TTSEngine.EDGE  # 默认使用Edge TTS
    
    # ============ 获取语音列表 ============
    
    async def get_voices(
        self, 
        engine: TTSEngine = None,
        language: str = None
    ) -> List[VoiceInfo]:
        """获取可用语音列表
        
        Args:
            engine: 引擎
            language: 语言筛选
        
        Returns:
            List[VoiceInfo]: 语音列表
        """
        if engine is None:
            engine = self.detect_engine()
        
        if engine == TTSEngine.EDGE:
            return await self._get_edge_voices(language)
        elif engine == TTSEngine.SAY:
            return await self._get_say_voices()
        elif engine == TTSEngine.ESPEAK:
            return await self._get_espeak_voices()
        else:
            return []
    
    async def _get_edge_voices(self, language: str = None) -> List[VoiceInfo]:
        """获取Edge TTS语音"""
        voices = [
            # 中文语音
            VoiceInfo("zh-CN-XiaoxiaoNeural", "晓晓", "Female", "zh-CN", "edge", "high"),
            VoiceInfo("zh-CN-XiaoyiNeural", "晓悠", "Female", "zh-CN", "edge", "high"),
            VoiceInfo("zh-CN-YunxiNeural", "云希", "Male", "zh-CN", "edge", "high"),
            VoiceInfo("zh-CN-YunyangNeural", "云扬", "Male", "zh-CN", "edge", "high"),
            VoiceInfo("zh-CN-YunzeNeural", "云泽", "Male", "zh-CN", "edge", "high"),
            
            # 英文语音
            VoiceInfo("en-US-AriaNeural", "Aria", "Female", "en-US", "edge", "high"),
            VoiceInfo("en-US-GuyNeural", "Guy", "Male", "en-US", "edge", "high"),
            VoiceInfo("en-US-JennyNeural", "Jenny", "Female", "en-US", "edge", "high"),
            
            # 日文语音
            VoiceInfo("ja-JP-NanamiNeural", "Nanami", "Female", "ja-JP", "edge", "high"),
            VoiceInfo("ja-JP-KeitaNeural", "Keita", "Male", "ja-JP", "edge", "high"),
        ]
        
        if language:
            voices = [v for v in voices if v.language.lower() == language.lower()]
        
        return voices
    
    async def _get_say_voices(self) -> List[VoiceInfo]:
        """获取macOS say语音"""
        voices = []
        
        try:
            result = await asyncio.create_subprocess_shell(
                "say -v '?'",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            output, _ = await result.communicate()
            
            for line in output.decode().strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    info = ' '.join(parts[1:])
                    
                    # 提取语言
                    lang = "unknown"
                    if "Chinese" in info:
                        lang = "zh-CN"
                    elif "English" in info:
                        lang = "en-US"
                    elif "Japanese" in info:
                        lang = "ja-JP"
                    
                    gender = "Female" if "female" in info.lower() else "Male"
                    
                    voices.append(VoiceInfo(
                        id=name,
                        name=name,
                        gender=gender,
                        language=lang,
                        engine="say",
                        quality="medium"
                    ))
        except Exception as e:
            print(f"获取macOS语音失败: {e}")
        
        return voices
    
    async def _get_espeak_voices(self) -> List[VoiceInfo]:
        """获取eSpeak语音"""
        voices = [
            VoiceInfo("zh", "Chinese", "Male", "zh-CN", "espeak", "low"),
            VoiceInfo("zh-CN", "Chinese (Mandarin)", "Male", "zh-CN", "espeak", "low"),
            VoiceInfo("en", "English", "Male", "en-US", "espeak", "low"),
            VoiceInfo("en-US", "English (US)", "Male", "en-US", "espeak", "low"),
            VoiceInfo("ja", "Japanese", "Male", "ja-JP", "espeak", "low"),
        ]
        
        return voices
    
    # ============ 语音合成 ============
    
    async def synthesize(
        self,
        text: str,
        voice_id: str = None,
        engine: TTSEngine = None,
        language: str = "zh-CN",
        rate: float = 1.0,       # 语速 0.5-2.0
        pitch: int = 0,          # 音调 -20 to 20
        volume: float = 1.0,     # 音量 0-1
        output_path: str = None,
        format: str = "mp3"       # mp3, wav, ogg
    ) -> TTSResult:
        """语音合成
        
        Args:
            text: 要合成的文本
            voice_id: 语音ID
            engine: 引擎
            language: 语言
            rate: 语速
            pitch: 音调
            volume: 音量
            output_path: 输出文件路径
            format: 输出格式
        
        Returns:
            TTSResult: 合成结果
        """
        import time

        start_time = time.time()
        
        if engine is None:
            engine = self.detect_engine()
        
        if engine == TTSEngine.EDGE:
            return await self._synthesize_edge(
                text, voice_id, rate, pitch, volume, output_path, format, start_time
            )
        elif engine == TTSEngine.SAY:
            return await self._synthesize_say(
                text, voice_id, rate, pitch, output_path, start_time
            )
        elif engine == TTSEngine.ESPEAK:
            return await self._synthesize_espeak(
                text, voice_id, rate, pitch, volume, output_path, start_time
            )
        else:
            return await self._synthesize_edge(
                text, voice_id, rate, pitch, volume, output_path, format, start_time
            )
    
    async def _synthesize_edge(
        self,
        text: str,
        voice_id: str,
        rate: float,
        pitch: int,
        volume: float,
        output_path: str,
        format: str,
        start_time: float
    ) -> TTSResult:
        """Edge TTS合成"""
        try:
            import edge_tts
            import math
            
            # 默认中文语音
            if not voice_id:
                voice_id = "zh-CN-XiaoxiaoNeural"
            
            # 转换语速
            rate_str = f"{int(rate * 100)}%"
            if rate > 1.0:
                rate_str = f"+{int((rate - 1.0) * 100)}%"
            elif rate < 1.0:
                rate_str = f"-{int((1.0 - rate) * 100)}%"
            
            # 转换音调
            pitch_str = f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"
            
            # 转换音量
            volume_str = f"+{int((volume - 1.0) * 100)}%" if volume >= 1.0 else f"{int(volume * 100)}%"
            
            communicate = edge_tts.Communicate(
                text,
                voice_id,
                rate=rate_str,
                pitch=pitch_str,
                volume=volume_str
            )
            
            # 保存到文件或内存
            if output_path:
                await communicate.save(output_path)
                
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
            else:
                # 保存到临时文件
                temp_file = f"/tmp/tts_output.{format}"
                await communicate.save(temp_file)
                
                with open(temp_file, 'rb') as f:
                    audio_data = f.read()
            
            duration = time.time() - start_time
            
            return TTSResult(
                text=text,
                audio_data=audio_data,
                duration=duration,
                format=format,
                engine="edge",
                voice_id=voice_id,
                success=True
            )
            
        except Exception as e:
            print(f"Edge TTS失败: {e}")
            return TTSResult(
                text=text,
                audio_data=b'',
                duration=0,
                format=format,
                engine="edge",
                voice_id=voice_id or "zh-CN-XiaoxiaoNeural",
                success=False,
                error=str(e)
            )
    
    async def _synthesize_say(
        self,
        text: str,
        voice_id: str,
        rate: float,
        pitch: int,
        output_path: str,
        start_time: float
    ) -> TTSResult:
        """macOS say合成"""
        try:
            cmd = ["say"]
            
            if voice_id:
                cmd.extend(["-v", voice_id])
            
            # 语速
            cmd.extend(["-r", str(int(rate * 175))])
            
            if output_path:
                cmd.extend(["-o", output_path])
            
            cmd.append(text)
            
            result = await asyncio.create_subprocess_shell(
                ' '.join(cmd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            if output_path:
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
            else:
                audio_data = b''
            
            duration = time.time() - start_time
            
            return TTSResult(
                text=text,
                audio_data=audio_data,
                duration=duration,
                format="aiff",
                engine="say",
                voice_id=voice_id or "Victoria",
                success=True
            )
            
        except Exception as e:
            print(f"macOS say失败: {e}")
            return TTSResult(
                text=text,
                audio_data=b'',
                duration=0,
                format="aiff",
                engine="say",
                voice_id=voice_id,
                success=False,
                error=str(e)
            )
    
    async def _synthesize_espeak(
        self,
        text: str,
        voice_id: str,
        rate: float,
        pitch: int,
        volume: float,
        output_path: str,
        start_time: float
    ) -> TTSResult:
        """eSpeak合成"""
        try:
            cmd = ["espeak"]
            
            # 语言/语音
            if voice_id:
                cmd.extend(["-v", voice_id])
            else:
                cmd.extend(["-v", "zh"])
            
            # 语速 (words per minute, 默认 175)
            cmd.extend(["-s", str(int(rate * 175))])
            
            # 音调
            cmd.extend(["-p", str(pitch)])
            
            # 音量
            cmd.extend(["-a", str(int(volume * 100))])
            
            # 输出文件
            if output_path:
                cmd.extend(["-w", output_path])
            
            cmd.append(text)
            
            result = await asyncio.create_subprocess_shell(
                ' '.join(cmd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            if output_path:
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
            else:
                audio_data = b''
            
            duration = time.time() - start_time
            
            return TTSResult(
                text=text,
                audio_data=audio_data,
                duration=duration,
                format="wav",
                engine="espeak",
                voice_id=voice_id or "zh",
                success=True
            )
            
        except Exception as e:
            print(f"eSpeak失败: {e}")
            return TTSResult(
                text=text,
                audio_data=b'',
                duration=0,
                format="wav",
                engine="espeak",
                voice_id=voice_id or "zh",
                success=False,
                error=str(e)
            )
    
    # ============ 流式合成 ============
    
    async def synthesize_stream(
        self,
        text: str,
        engine: TTSEngine = None,
        voice_id: str = None,
        **kwargs
    ) -> AsyncIterator[bytes]:
        """流式语音合成
        
        Yields:
            bytes: 音频数据块
        """
        # Edge TTS支持流式
        if engine is None:
            engine = self.detect_engine()
        
        if engine == TTSEngine.EDGE:
            async for chunk in self._stream_edge(text, voice_id, **kwargs):
                yield chunk
    
    async def _stream_edge(
        self,
        text: str,
        voice_id: str,
        rate: float = 1.0,
        pitch: int = 0,
        **kwargs
    ) -> AsyncIterator[bytes]:
        """Edge TTS流式"""
        try:
            import edge_tts
            
            if not voice_id:
                voice_id = "zh-CN-XiaoxiaoNeural"
            
            rate_str = f"+{int((rate - 1.0) * 100)}%" if rate > 1.0 else f"{int(rate * 100)}%"
            
            communicate = edge_tts.Communicate(
                text, voice_id,
                rate=rate_str,
                pitch=f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"
            )
            
            async for chunk in communicate.stream():
                yield chunk
                
        except Exception as e:
            print(f"Edge TTS流式失败: {e}")
    
    # ============ 播放 ============
    
    async def play_audio(
        self,
        audio_data: bytes,
        output_path: str = None
    ):
        """播放音频
        
        Args:
            audio_data: 音频数据
            output_path: 临时文件路径
        """
        if self.platform == "Darwin":
            await self._play_macos(audio_data, output_path)
        elif self.platform == "Windows":
            await self._play_windows(audio_data, output_path)
        else:
            await self._play_linux(audio_data, output_path)
    
    async def _play_macos(self, audio_data: bytes, output_path: str = None):
        """macOS播放"""
        try:
            if not output_path:
                output_path = "/tmp/tts_output.aiff"
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            await asyncio.create_subprocess_shell(
                f"afplay {output_path}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        except Exception as e:
            print(f"macOS播放失败: {e}")
    
    async def _play_windows(self, audio_data: bytes, output_path: str = None):
        """Windows播放"""
        try:
            import winsound
            import io
            from scipy.io import wavfile
            
            # 简单实现 - 使用默认播放
            pass
        except Exception as e:
            print(f"Windows播放失败: {e}")
    
    async def _play_linux(self, audio_data: bytes, output_path: str = None):
        """Linux播放"""
        try:
            if not output_path:
                output_path = "/tmp/tts_output.wav"
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            # 使用aplay或ffplay
            try:
                await asyncio.create_subprocess_shell(
                    f"ffplay -autoexit -nodisp {output_path}",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
            except:
                await asyncio.create_subprocess_shell(
                    f"aplay {output_path}",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
        except Exception as e:
            print(f"Linux播放失败: {e}")
    
    # ============ 便捷方法 ============
    
    async def speak(
        self,
        text: str,
        language: str = "zh-CN",
        voice_id: str = None
    ):
        """直接说话 (合成并播放)
        
        Args:
            text: 要说的文本
            language: 语言
            voice_id: 语音
        """
        engine = self.detect_engine()
        
        result = await self.synthesize(
            text,
            voice_id=voice_id,
            engine=engine,
            language=language
        )
        
        if result.success:
            await self.play_audio(result.audio_data)
        else:
            print(f"语音合成失败: {result.error}")
    
    def text_to_base64(self, audio_data: bytes) -> str:
        """音频转Base64"""
        return base64.b64encode(audio_data).decode()
    
    def base64_to_text(self, base64_str: str) -> bytes:
        """Base64转音频"""
        return base64.b64decode(base64_str.encode())


# 便捷函数
async def speak(text: str, language: str = "zh-CN"):
    """直接说话"""
    tts = TextToSpeech()
    await tts.speak(text, language)

async def text_to_speech(
    text: str,
    voice_id: str = None,
    output_path: str = None
) -> TTSResult:
    """文字转语音"""
    tts = TextToSpeech()
    return await tts.synthesize(text, voice_id=voice_id, output_path=output_path)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("🔊 语音合成测试")
        
        tts = TextToSpeech()
        
        # 检测引擎
        engine = tts.detect_engine()
        print(f"   可用引擎: {engine.value}")
        
        # 获取语音列表
        print("\n📋 中文语音:")
        voices = await tts.get_voices(engine=engine, language="zh-CN")
        for voice in voices[:3]:
            print(f"   - {voice.name} ({voice.gender})")
        
        # 测试语音合成
        print("\n🔊 测试语音合成...")
        result = await tts.synthesize(
            "你好,我是ClawOS AI助手!",
            voice_id="zh-CN-XiaoxiaoNeural",
            rate=1.0
        )
        
        if result.success:
            print(f"   ✅ 合成成功! 时长: {result.duration:.2f}秒")
            print(f"   🎵 音频大小: {len(result.audio_data)} bytes")
        else:
            print(f"   ❌ 合成失败: {result.error}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
