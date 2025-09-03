import subprocess
import json
import asyncio
import dns.resolver
import whois
import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import socket
import re

class ReconService:
    """Service for reconnaissance and footprinting operations"""
    
    def __init__(self):
        self.timeout = 30
    
    async def enumerate_subdomains(self, domain: str, tools: List[str]) -> Dict[str, Any]:
        """Enumerate subdomains using specified tools"""
        results = {"subdomains": set(), "live_subdomains": []}
        
        for tool in tools:
            if tool == "subfinder":
                subdomains = await self._run_subfinder(domain)
                results["subdomains"].update(subdomains)
            elif tool == "amass":
                subdomains = await self._run_amass(domain)
                results["subdomains"].update(subdomains)
            elif tool == "sublist3r":
                subdomains = await self._run_sublist3r(domain)
                results["subdomains"].update(subdomains)
        
        # Convert set to list
        results["subdomains"] = list(results["subdomains"])
        
        # Check which subdomains are live
        results["live_subdomains"] = await self._check_live_subdomains(results["subdomains"])
        
        return results
    
    def enumerate_subdomains_sync(self, domain: str, tools: List[str]) -> Dict[str, Any]:
        """Synchronous version for Celery tasks"""
        return asyncio.run(self.enumerate_subdomains(domain, tools))
    
    async def _run_subfinder(self, domain: str) -> List[str]:
        """Run subfinder tool"""
        try:
            # For now, return mock data since subfinder might not be installed
            # In production, you would run: subfinder -d domain -silent
            return [f"www.{domain}", f"mail.{domain}", f"ftp.{domain}"]
        except Exception:
            return []
    
    async def _run_amass(self, domain: str) -> List[str]:
        """Run amass tool"""
        try:
            # Mock data - in production: amass enum -d domain
            return [f"api.{domain}", f"admin.{domain}", f"test.{domain}"]
        except Exception:
            return []
    
    async def _run_sublist3r(self, domain: str) -> List[str]:
        """Run sublist3r tool"""
        try:
            # Mock data - in production: sublist3r -d domain
            return [f"blog.{domain}", f"shop.{domain}", f"dev.{domain}"]
        except Exception:
            return []
    
    async def _check_live_subdomains(self, subdomains: List[str]) -> List[str]:
        """Check which subdomains are live"""
        live = []
        for subdomain in subdomains:
            try:
                # Simple HTTP check
                response = requests.get(f"http://{subdomain}", timeout=5)
                if response.status_code < 400:
                    live.append(subdomain)
            except:
                try:
                    # Try HTTPS
                    response = requests.get(f"https://{subdomain}", timeout=5)
                    if response.status_code < 400:
                        live.append(subdomain)
                except:
                    pass
        return live
    
    async def port_scan(self, target: str, scan_type: str = "fast", ports: Optional[str] = None) -> Dict[str, Any]:
        """Perform port scanning"""
        try:
            if scan_type == "fast":
                port_list = "22,80,443,21,25,53,110,143,993,995,8080,8443"
            elif scan_type == "full":
                port_list = "1-65535"
            else:
                port_list = ports or "80,443"
            
            # Use nmap for port scanning
            cmd = f"nmap -sS -T4 -p {port_list} {target}"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return self._parse_nmap_output(stdout.decode())
            else:
                # Fallback to basic socket scan for common ports
                return await self._basic_port_scan(target, [80, 443, 22, 21, 25])
                
        except Exception as e:
            return {"error": str(e), "open_ports": [], "services": {}}
    
    def port_scan_sync(self, target: str, scan_type: str = "fast") -> Dict[str, Any]:
        """Synchronous version for Celery tasks"""
        return asyncio.run(self.port_scan(target, scan_type))
    
    def _parse_nmap_output(self, output: str) -> Dict[str, Any]:
        """Parse nmap output"""
        open_ports = []
        services = {}
        
        lines = output.split('\n')
        for line in lines:
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 2:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else "unknown"
                    open_ports.append(int(port))
                    services[port] = service
        
        return {
            "open_ports": open_ports,
            "services": services,
            "total_scanned": len(open_ports)
        }
    
    async def _basic_port_scan(self, target: str, ports: List[int]) -> Dict[str, Any]:
        """Basic port scan using sockets"""
        open_ports = []
        services = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    services[str(port)] = self._guess_service(port)
                sock.close()
            except:
                pass
        
        return {
            "open_ports": open_ports,
            "services": services,
            "total_scanned": len(ports)
        }
    
    def _guess_service(self, port: int) -> str:
        """Guess service based on port number"""
        common_ports = {
            22: "ssh",
            21: "ftp",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            993: "imaps",
            995: "pop3s",
            8080: "http-alt",
            8443: "https-alt"
        }
        return common_ports.get(port, "unknown")
    
    async def detect_tech_stack(self, url: str) -> Dict[str, Any]:
        """Detect technology stack of a website"""
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            content = response.text.lower()
            
            technologies = []
            cms = None
            web_server = headers.get('Server', 'Unknown')
            programming_languages = []
            frameworks = []
            
            # Detect CMS
            if 'wp-content' in content or 'wordpress' in content:
                cms = "WordPress"
                technologies.append("WordPress")
            elif 'drupal' in content:
                cms = "Drupal"
                technologies.append("Drupal")
            elif 'joomla' in content:
                cms = "Joomla"
                technologies.append("Joomla")
            
            # Detect technologies from headers
            if 'php' in headers.get('X-Powered-By', '').lower():
                programming_languages.append("PHP")
            
            # Detect from content
            if 'react' in content:
                frameworks.append("React")
            if 'angular' in content:
                frameworks.append("Angular")
            if 'vue' in content:
                frameworks.append("Vue.js")
            
            return {
                "technologies": technologies,
                "cms": cms,
                "web_server": web_server,
                "programming_languages": programming_languages,
                "frameworks": frameworks
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def detect_tech_stack_sync(self, url: str) -> Dict[str, Any]:
        """Synchronous version for Celery tasks"""
        return asyncio.run(self.detect_tech_stack(url))

class DNSService:
    """Service for DNS operations"""
    
    async def lookup(self, domain: str, record_type: str = "A") -> List[str]:
        """Perform DNS lookup"""
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [str(answer) for answer in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

class WhoisService:
    """Service for WHOIS operations"""
    
    async def lookup(self, domain: str) -> Dict[str, Any]:
        """Perform WHOIS lookup"""
        try:
            w = whois.whois(domain)
            return {
                "domain": domain,
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "name_servers": w.name_servers if w.name_servers else [],
                "status": w.status if w.status else [],
                "emails": w.emails if w.emails else [],
                "country": w.country if hasattr(w, 'country') else None
            }
        except Exception as e:
            return {"error": str(e)}