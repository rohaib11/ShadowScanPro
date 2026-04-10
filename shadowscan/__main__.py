#!/usr/bin/env python3
"""
SHADOWSCAN PRO - Main Entry Point
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shadowscan.core.engine import ShadowEngine
from shadowscan.dashboard.cli_dashboard import AttackDashboard
from rich.console import Console

console = Console()
dashboard = AttackDashboard()


class ShadowCLI:
    """Command Line Interface for ShadowScan Pro"""
    
    def __init__(self):
        self.engine = None
        
    def show_banner(self):
        """Display the epic banner"""
        banner = f"""
[bold red]╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗ ██████╗ █████╗ ███╗   ██╗  ║
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗████╗  ██║  ║
║   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████╗██║     ███████║██╔██╗ ██║  ║
║   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════██║██║     ██╔══██║██║╚██╗██║  ║
║   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████║╚██████╗██║  ██║██║ ╚████║  ║
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ║
║                                                                              ║
║                    [bold yellow]🔥 SHADOWSCAN PRO - OFFENSIVE SECURITY 🔥[/bold yellow]                  ║
║                                                                              ║
║              [bold cyan]⚡ ROHAIB TECHNICAL ⚡[/bold cyan] | [bold green]📞 +92 306 3844400 📞[/bold green]                 ║
║                                                                              ║
║     [dim]"The tool that doesn't just find vulnerabilities - it EXPLOITS them"[/dim]     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝[/bold red]
        """
        console.print(banner)
    
    def create_parser(self):
        parser = argparse.ArgumentParser(
            description="SHADOWSCAN PRO - Offensive Security Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  shadowscan exploit --target example.com --auto
  shadowscan scan --target 192.168.1.0/24 --aggressive
  shadowscan cloud --scan-misconfigs
  shadowscan darkweb --query "company.com"
  shadowscan post-exploit --session shell-1 --auto-persist
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # Exploit command
        exploit_parser = subparsers.add_parser("exploit", help="Auto-exploitation mode")
        exploit_parser.add_argument("--target", "-t", required=True, help="Target URL/IP")
        exploit_parser.add_argument("--auto", action="store_true", help="Auto-exploit mode")
        exploit_parser.add_argument("--aggressive", action="store_true", help="Aggressive scanning")
        exploit_parser.add_argument("--stealth", action="store_true", help="Stealth mode")
        exploit_parser.add_argument("--tor", action="store_true", help="Route through Tor")
        exploit_parser.add_argument("--payload", choices=["reverse_shell", "bind_shell", "meterpreter"], default="reverse_shell")
        
        # Scan command
        scan_parser = subparsers.add_parser("scan", help="Vulnerability scanning")
        scan_parser.add_argument("--target", "-t", required=True)
        scan_parser.add_argument("--ports", "-p", help="Port range (e.g., 1-1000)")
        scan_parser.add_argument("--aggressive", action="store_true")
        scan_parser.add_argument("--service-detection", action="store_true")
        
        # Cloud command
        cloud_parser = subparsers.add_parser("cloud", help="Cloud exploitation")
        cloud_parser.add_argument("--scan-misconfigs", action="store_true")
        cloud_parser.add_argument("--target-bucket", help="Target S3 bucket")
        cloud_parser.add_argument("--enum-buckets", action="store_true")
        
        # Darkweb command
        darkweb_parser = subparsers.add_parser("darkweb", help="Dark web intelligence")
        darkweb_parser.add_argument("--query", "-q", required=True)
        darkweb_parser.add_argument("--tor", action="store_true", default=True)
        darkweb_parser.add_argument("--deep", action="store_true")
        
        # Post-exploit command
        post_parser = subparsers.add_parser("post-exploit", help="Post-exploitation")
        post_parser.add_argument("--session", "-s", help="Session ID")
        post_parser.add_argument("--auto-persist", action="store_true")
        post_parser.add_argument("--harvest-creds", action="store_true")
        post_parser.add_argument("--lateral-move", action="store_true")
        post_parser.add_argument("--privesc", action="store_true")
        
        # Interactive mode
        subparsers.add_parser("interactive", help="Interactive attack console")
        
        return parser
    
    async def run_exploit(self, args):
        """Run auto-exploitation"""
        dashboard.show_banner()
        
        self.engine = ShadowEngine(
            target=args.target,
            mode="exploit",
            aggressive=args.aggressive,
            stealth=args.stealth,
            use_tor=args.tor
        )
        
        if args.auto:
            await self.engine.auto_exploit(payload_type=args.payload)
        else:
            await self.engine.manual_exploit()
    
    async def run_scan(self, args):
        """Run vulnerability scan"""
        dashboard.show_banner()
        
        self.engine = ShadowEngine(
            target=args.target,
            mode="scan",
            aggressive=args.aggressive
        )
        
        await self.engine.vulnerability_scan(ports=args.ports)
    
    async def run_cloud(self, args):
        """Run cloud exploitation"""
        dashboard.show_banner()
        
        self.engine = ShadowEngine(target="cloud", mode="cloud")
        
        if args.scan_misconfigs:
            await self.engine.scan_cloud_misconfigs()
        elif args.target_bucket:
            await self.engine.exploit_bucket(args.target_bucket)
    
    async def run_darkweb(self, args):
        """Run dark web search"""
        dashboard.show_banner()
        
        self.engine = ShadowEngine(target=args.query, mode="darkweb", use_tor=args.tor)
        await self.engine.darkweb_search(deep=args.deep)
    
    async def run_post_exploit(self, args):
        """Run post-exploitation"""
        dashboard.show_banner()
        
        self.engine = ShadowEngine(target=args.session, mode="post_exploit")
        
        if args.auto_persist:
            await self.engine.auto_persistence()
        if args.harvest_creds:
            await self.engine.harvest_credentials()
        if args.lateral_move:
            await self.engine.lateral_movement()
        if args.privesc:
            await self.engine.privilege_escalation()
    
    async def run_interactive(self):
        """Run interactive mode"""
        dashboard.show_banner()
        await dashboard.start_interactive_console()
    
    async def main(self):
        parser = self.create_parser()
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            if args.command == "exploit":
                await self.run_exploit(args)
            elif args.command == "scan":
                await self.run_scan(args)
            elif args.command == "cloud":
                await self.run_cloud(args)
            elif args.command == "darkweb":
                await self.run_darkweb(args)
            elif args.command == "post-exploit":
                await self.run_post_exploit(args)
            elif args.command == "interactive":
                await self.run_interactive()
                
        except KeyboardInterrupt:
            console.print("\n[yellow][!] Attack interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"[red][✗] Error: {e}[/red]")
            sys.exit(1)


def main():
    cli = ShadowCLI()
    asyncio.run(cli.main())


if __name__ == "__main__":
    main()