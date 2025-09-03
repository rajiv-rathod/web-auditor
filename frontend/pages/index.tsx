import { useState, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { 
  ShieldCheckIcon, 
  CpuChipIcon, 
  BugAntIcon, 
  DocumentArrowDownIcon,
  EyeIcon,
  ServerIcon 
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function Home() {
  const [user, setUser] = useState(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
    }
  }, [router])

  const features = [
    {
      name: 'Reconnaissance',
      description: 'Subdomain enumeration, DNS lookup, port scanning, and technology fingerprinting',
      icon: EyeIcon,
      href: '/recon',
      color: 'bg-blue-500'
    },
    {
      name: 'Vulnerability Testing',
      description: 'SQL injection, XSS detection, directory bruteforce, and CMS security scanning',
      icon: BugAntIcon,
      href: '/vulnerability',
      color: 'bg-red-500'
    },
    {
      name: 'Infrastructure Scanning',
      description: 'Port scanning, service enumeration, and network discovery',
      icon: ServerIcon,
      href: '/infrastructure',
      color: 'bg-green-500'
    },
    {
      name: 'Technology Detection',
      description: 'Web technology stack identification and version detection',
      icon: CpuChipIcon,
      href: '/tech-stack',
      color: 'bg-purple-500'
    },
    {
      name: 'Security Assessment',
      description: 'Comprehensive security analysis and vulnerability assessment',
      icon: ShieldCheckIcon,
      href: '/assessment',
      color: 'bg-orange-500'
    },
    {
      name: 'Reports',
      description: 'Generate detailed security reports in PDF and HTML formats',
      icon: DocumentArrowDownIcon,
      href: '/reports',
      color: 'bg-indigo-500'
    }
  ]

  return (
    <>
      <Head>
        <title>Web Auditor - Comprehensive Security Testing Platform</title>
        <meta name="description" content="Professional web security auditing and penetration testing platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <ShieldCheckIcon className="h-8 w-8 text-blue-600" />
                <span className="ml-2 text-xl font-bold text-gray-900">Web Auditor</span>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/scans" className="text-gray-700 hover:text-gray-900">
                  My Scans
                </Link>
                <Link href="/reports" className="text-gray-700 hover:text-gray-900">
                  Reports
                </Link>
                <button
                  onClick={() => {
                    localStorage.removeItem('token')
                    router.push('/login')
                  }}
                  className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600">
          <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl font-extrabold text-white sm:text-5xl">
                Comprehensive Web Security Auditing
              </h1>
              <p className="mt-4 text-xl text-blue-100">
                Professional-grade security testing tools for modern web applications
              </p>
              <div className="mt-8">
                <Link
                  href="/recon"
                  className="bg-white text-blue-600 px-8 py-3 rounded-md text-lg font-medium hover:bg-gray-50 transition-colors"
                >
                  Start Security Audit
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Security Testing Features
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Complete toolkit for web application security assessment
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <Link key={feature.name} href={feature.href}>
                <div className="relative group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                  <div>
                    <span className={`rounded-lg inline-flex p-3 ${feature.color} text-white`}>
                      <feature.icon className="h-6 w-6" />
                    </span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium text-gray-900 group-hover:text-blue-600">
                      {feature.name}
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div className="bg-white">
          <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">50+</div>
                <div className="text-sm text-gray-600">Security Tools</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">10,000+</div>
                <div className="text-sm text-gray-600">Vulnerabilities Detected</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">500+</div>
                <div className="text-sm text-gray-600">Reports Generated</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">99.9%</div>
                <div className="text-sm text-gray-600">Uptime</div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="bg-gray-800">
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <div className="text-center text-gray-400">
              <p>&copy; 2024 Web Auditor. Professional Security Testing Platform.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}