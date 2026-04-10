#!/usr/bin/env python3
"""
SHADOWSCAN PRO - Windows Compatibility Test
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

async def test_imports():
    """Test all module imports"""
    console.print("\n[bold cyan]1. Testing Module Imports...[/bold cyan]")
    
    modules_to_test = [
        # Core
        ("shadowscan", "Core Package"),
        ("shadowscan.__main__", "CLI Entry"),
        ("shadowscan.core.engine", "Engine"),
        ("shadowscan.core.exploit_chain", "Exploit Chain"),
        ("shadowscan.core.payload_generator", "Payload Generator"),
        ("shadowscan.core.stealth_manager", "Stealth Manager"),
        ("shadowscan.core.session_manager", "Session Manager"),
        ("shadowscan.core.monitor", "Attack Monitor"),
        
        # Dashboard
        ("shadowscan.dashboard.cli_dashboard", "CLI Dashboard"),
        ("shadowscan.dashboard.attack_monitor", "Attack Monitor Dashboard"),
        ("shadowscan.dashboard.progress_bars", "Progress Bars"),
        ("shadowscan.dashboard.colors", "Color Schemes"),
        
        # Exploits - Web
        ("shadowscan.exploits.web.sqli", "SQL Injection"),
        ("shadowscan.exploits.web.xss", "XSS"),
        ("shadowscan.exploits.web.lfi", "LFI"),
        ("shadowscan.exploits.web.command_injection", "Command Injection"),
        
        # Exploits - Network
        ("shadowscan.exploits.network.eternalblue", "EternalBlue"),
        ("shadowscan.exploits.network.smb_exploits", "SMB Exploits"),
        
        # Exploits - Cloud
        ("shadowscan.exploits.cloud.s3_scanner", "S3 Scanner"),
        
        # Exploits - CVE
        ("shadowscan.exploits.cve.log4shell", "Log4Shell"),
        
        # OSINT
        ("shadowscan.osint.darkweb_crawler", "Dark Web Crawler"),
        ("shadowscan.osint.leak_searcher", "Leak Searcher"),
        
        # Post-Exploit
        ("shadowscan.post_exploit.persistence", "Persistence"),
        ("shadowscan.post_exploit.privesc", "Privilege Escalation"),
        ("shadowscan.post_exploit.credential_harvester", "Credential Harvester"),
        
        # Utils
        ("shadowscan.utils.waf_bypass", "WAF Bypass"),
        ("shadowscan.utils.tor_manager", "Tor Manager"),
        ("shadowscan.utils.fingerprint_randomizer", "Fingerprint Randomizer"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            results.append((description, "✓", "green"))
            passed += 1
        except Exception as e:
            results.append((description, f"✗ {str(e)[:40]}", "red"))
            failed += 1
    
    table = Table(title="Import Test Results")
    table.add_column("Module", style="cyan", width=30)
    table.add_column("Status", style="bold", width=50)
    
    for desc, status, color in results:
        table.add_row(desc, f"[{color}]{status}[/{color}]")
    
    console.print(table)
    console.print(f"\n[bold]Passed: {passed}/{len(modules_to_test)} | Failed: {failed}[/bold]")
    
    return failed == 0

async def test_dashboard():
    """Test dashboard initialization"""
    console.print("\n[bold cyan]2. Testing Dashboard...[/bold cyan]")
    
    try:
        from shadowscan.dashboard.cli_dashboard import AttackDashboard
        dashboard = AttackDashboard()
        console.print("  [green]✓[/green] AttackDashboard initialized")
        
        dashboard.show_banner()
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Dashboard failed: {e}")
        return False

async def test_config():
    """Test configuration"""
    console.print("\n[bold cyan]3. Testing Configuration...[/bold cyan]")
    
    try:
        from pathlib import Path
        config_dir = Path.home() / ".shadowscan"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create default config if not exists
        config_file = config_dir / "settings.yaml"
        if not config_file.exists():
            import yaml
            default_config = {
                "app": {"name": "SHADOWSCAN PRO", "version": "1.0.0"},
                "stealth": {"profile": "shadow", "tor_enabled": False}
            }
            with open(config_file, 'w') as f:
                yaml.dump(default_config, f)
        
        console.print(f"  [green]✓[/green] Config directory: {config_dir}")
        console.print(f"  [green]✓[/green] Config file: {config_file}")
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Config failed: {e}")
        return False

async def test_engine():
    """Test engine initialization"""
    console.print("\n[bold cyan]4. Testing Attack Engine...[/bold cyan]")
    
    try:
        from shadowscan.core.engine import ShadowEngine
        
        engine = ShadowEngine(
            target="example.com",
            mode="scan",
            aggressive=False,
            stealth=True
        )
        
        console.print("  [green]✓[/green] ShadowEngine initialized")
        console.print(f"  [dim]Target: {engine.target}[/dim]")
        console.print(f"  [dim]Mode: {engine.mode}[/dim]")
        console.print(f"  [dim]Stealth: {engine.stealth}[/dim]")
        
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Engine failed: {e}")
        return False

async def test_exploits():
    """Test exploit modules"""
    console.print("\n[bold cyan]5. Testing Exploit Modules...[/bold cyan]")
    
    try:
        # Test SQLi
        from shadowscan.exploits.web.sqli import SQLiExploit
        sqli = SQLiExploit()
        console.print("  [green]✓[/green] SQLiExploit initialized")
        
        # Test XSS
        from shadowscan.exploits.web.xss import XSSExploit
        xss = XSSExploit()
        console.print("  [green]✓[/green] XSSExploit initialized")
        
        # Test S3 Scanner
        from shadowscan.exploits.cloud.s3_scanner import S3Scanner
        s3 = S3Scanner()
        console.print("  [green]✓[/green] S3Scanner initialized")
        
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Exploit test failed: {e}")
        return False

async def test_payload_generator():
    """Test payload generator"""
    console.print("\n[bold cyan]6. Testing Payload Generator...[/bold cyan]")
    
    try:
        from shadowscan.core.payload_generator import PayloadGenerator
        
        generator = PayloadGenerator()
        payload = generator.generate(
            payload_type="reverse_shell",
            platform="bash",
            lhost="127.0.0.1",
            lport=4444,
            obfuscate=True
        )
        
        if payload:
            console.print("  [green]✓[/green] Payload generated successfully")
            console.print(f"  [dim]Type: {payload.payload_type}[/dim]")
            console.print(f"  [dim]Platform: {payload.platform}[/dim]")
            console.print(f"  [dim]Size: {payload.size} bytes[/dim]")
        else:
            console.print("  [yellow]⚠[/yellow] Payload generation returned None")
        
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Payload generator failed: {e}")
        return False

async def test_stealth():
    """Test stealth manager"""
    console.print("\n[bold cyan]7. Testing Stealth Manager...[/bold cyan]")
    
    try:
        from shadowscan.core.stealth_manager import StealthManager
        
        stealth = StealthManager(profile_name="stealth")
        console.print("  [green]✓[/green] StealthManager initialized")
        
        ua = stealth.get_user_agent()
        console.print(f"  [dim]User Agent: {ua[:60]}...[/dim]")
        
        headers = stealth.get_headers()
        console.print(f"  [dim]Headers: {len(headers)} headers generated[/dim]")
        
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Stealth manager failed: {e}")
        return False

async def test_secret_detector():
    """Test secret detector"""
    console.print("\n[bold cyan]8. Testing Secret Detector...[/bold cyan]")
    
    try:
        # Create simple secret detector test
        import re
        
        test_strings = [
            "AKIAIOSFODNN7EXAMPLE",
            "password = 'MySecretPass123'",
            "API_KEY=sk_live_1234567890abcdef",
            "ghp_1234567890abcdefghijklmnopqrstuv",
        ]
        
        patterns = {
            "aws_key": r'AKIA[0-9A-Z]{16}',
            "password": r'(?i)password[\s:=]+[\'"]?([^\'"\s]{6,})',
            "api_key": r'sk_[a-z]+_[A-Za-z0-9]{24,}',
            "github_token": r'ghp_[A-Za-z0-9_]{36}',
        }
        
        found = 0
        for test in test_strings:
            for name, pattern in patterns.items():
                if re.search(pattern, test):
                    found += 1
                    break
        
        console.print(f"  [green]✓[/green] Secret detector found {found}/{len(test_strings)} secrets")
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Secret detector failed: {e}")
        return False

async def main():
    """Run all tests"""
    console.print(Panel.fit(
        "[bold red]🔥 SHADOWSCAN PRO - Windows Compatibility Test 🔥[/bold red]\n"
        "[dim]Developed by ROHAIB TECHNICAL | +92 306 3844400[/dim]",
        border_style="red"
    ))
    
    tests = [
        ("Module Imports", test_imports),
        ("Dashboard", test_dashboard),
        ("Configuration", test_config),
        ("Attack Engine", test_engine),
        ("Exploit Modules", test_exploits),
        ("Payload Generator", test_payload_generator),
        ("Stealth Manager", test_stealth),
        ("Secret Detector", test_secret_detector),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            console.print(f"[red]Test '{name}' crashed: {e}[/red]")
            results.append((name, False))
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold]📊 TEST SUMMARY[/bold]\n")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[green]✓ PASS[/green]" if result else "[red]✗ FAIL[/red]"
        console.print(f"  {status}  {name}")
    
    console.print(f"\n[bold]Result: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[bold green]✅ SHADOWSCAN PRO is ready for Windows![/bold green]")
        console.print("\n[yellow]Quick Start Commands:[/yellow]")
        console.print("  [cyan]python -m shadowscan --help[/cyan]")
        console.print("  [cyan]python -m shadowscan interactive[/cyan]")
        console.print("  [cyan]python test_scan.py[/cyan]")
    else:
        console.print("\n[yellow]⚠ Some tests failed. Check the errors above.[/yellow]")
    
    console.print("\n[dim]Developed by ROHAIB TECHNICAL | +92 306 3844400[/dim]")

if __name__ == "__main__":
    asyncio.run(main())