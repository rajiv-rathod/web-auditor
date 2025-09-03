import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { reconApi } from '../lib/api'
import { 
  ShieldCheckIcon, 
  EyeIcon, 
  GlobeAltIcon, 
  ServerIcon,
  CpuChipIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'

interface ReconForm {
  domain: string
  target: string
  url: string
}

export default function Recon() {
  const [loading, setLoading] = useState<string | null>(null)
  const [results, setResults] = useState<any>({})
  const { register, handleSubmit, formState: { errors } } = useForm<ReconForm>()

  const runSubdomainScan = async (data: ReconForm) => {
    setLoading('subdomain')
    try {
      const response = await reconApi.subdomainScan(data.domain)
      setResults(prev => ({ ...prev, subdomain: response.data }))
      toast.success('Subdomain scan completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Subdomain scan failed')
    } finally {
      setLoading(null)
    }
  }

  const runPortScan = async (data: ReconForm) => {
    setLoading('port')
    try {
      const response = await reconApi.portScan(data.target)
      setResults(prev => ({ ...prev, port: response.data }))
      toast.success('Port scan completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Port scan failed')
    } finally {
      setLoading(null)
    }
  }

  const runDNSLookup = async (data: ReconForm) => {
    setLoading('dns')
    try {
      const response = await reconApi.dnsLookup(data.domain)
      setResults(prev => ({ ...prev, dns: response.data }))
      toast.success('DNS lookup completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'DNS lookup failed')
    } finally {
      setLoading(null)
    }
  }

  const runWhoisLookup = async (data: ReconForm) => {
    setLoading('whois')
    try {
      const response = await reconApi.whoisLookup(data.domain)
      setResults(prev => ({ ...prev, whois: response.data }))
      toast.success('WHOIS lookup completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'WHOIS lookup failed')
    } finally {
      setLoading(null)
    }
  }

  const runTechStackScan = async (data: ReconForm) => {
    setLoading('techstack')
    try {
      const response = await reconApi.techStack(data.url)
      setResults(prev => ({ ...prev, techstack: response.data }))
      toast.success('Technology stack scan completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Tech stack scan failed')
    } finally {
      setLoading(null)
    }
  }

  return (
    <>
      <Head>
        <title>Reconnaissance - Web Auditor</title>
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link href="/">
                  <ShieldCheckIcon className="h-8 w-8 text-blue-600 cursor-pointer" />
                </Link>
                <span className="ml-2 text-xl font-bold text-gray-900">Web Auditor</span>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/" className="text-gray-700 hover:text-gray-900">
                  Dashboard
                </Link>
                <Link href="/vulnerability" className="text-gray-700 hover:text-gray-900">
                  Vulnerability
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <EyeIcon className="h-8 w-8 mr-3 text-blue-600" />
              Reconnaissance & Footprinting
            </h1>
            <p className="mt-2 text-gray-600">
              Gather information about your target domain and infrastructure
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Forms */}
            <div className="space-y-6">
              {/* Subdomain Enumeration */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                  <GlobeAltIcon className="h-5 w-5 mr-2 text-blue-600" />
                  Subdomain Enumeration
                </h3>
                <form onSubmit={handleSubmit(runSubdomainScan)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Domain</label>
                    <input
                      {...register('domain', { required: 'Domain is required' })}
                      type="text"
                      placeholder="example.com"
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
                    />
                    {errors.domain && <p className="text-red-600 text-sm">{errors.domain.message}</p>}
                  </div>
                  <button
                    type="submit"
                    disabled={loading === 'subdomain'}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {loading === 'subdomain' ? 'Scanning...' : 'Start Subdomain Scan'}
                  </button>
                </form>
              </div>

              {/* Port Scanning */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                  <ServerIcon className="h-5 w-5 mr-2 text-green-600" />
                  Port Scanning
                </h3>
                <form onSubmit={handleSubmit(runPortScan)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Target</label>
                    <input
                      {...register('target', { required: 'Target is required' })}
                      type="text"
                      placeholder="example.com or 192.168.1.1"
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
                    />
                    {errors.target && <p className="text-red-600 text-sm">{errors.target.message}</p>}
                  </div>
                  <button
                    type="submit"
                    disabled={loading === 'port'}
                    className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50"
                  >
                    {loading === 'port' ? 'Scanning...' : 'Start Port Scan'}
                  </button>
                </form>
              </div>

              {/* DNS Lookup */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                  <DocumentTextIcon className="h-5 w-5 mr-2 text-purple-600" />
                  DNS & WHOIS Lookup
                </h3>
                <div className="space-y-4">
                  <button
                    onClick={handleSubmit(runDNSLookup)}
                    disabled={loading === 'dns'}
                    className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50"
                  >
                    {loading === 'dns' ? 'Looking up...' : 'DNS Lookup'}
                  </button>
                  <button
                    onClick={handleSubmit(runWhoisLookup)}
                    disabled={loading === 'whois'}
                    className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {loading === 'whois' ? 'Looking up...' : 'WHOIS Lookup'}
                  </button>
                </div>
              </div>

              {/* Technology Stack */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                  <CpuChipIcon className="h-5 w-5 mr-2 text-orange-600" />
                  Technology Stack Detection
                </h3>
                <form onSubmit={handleSubmit(runTechStackScan)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">URL</label>
                    <input
                      {...register('url', { required: 'URL is required' })}
                      type="url"
                      placeholder="https://example.com"
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
                    />
                    {errors.url && <p className="text-red-600 text-sm">{errors.url.message}</p>}
                  </div>
                  <button
                    type="submit"
                    disabled={loading === 'techstack'}
                    className="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 disabled:opacity-50"
                  >
                    {loading === 'techstack' ? 'Scanning...' : 'Detect Tech Stack'}
                  </button>
                </form>
              </div>
            </div>

            {/* Results */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Scan Results</h3>
                
                {Object.keys(results).length === 0 ? (
                  <p className="text-gray-500">No scans performed yet. Start a scan to see results.</p>
                ) : (
                  <div className="space-y-6">
                    {/* Subdomain Results */}
                    {results.subdomain && (
                      <div>
                        <h4 className="font-medium text-blue-600 mb-2">Subdomain Enumeration</h4>
                        <div className="bg-gray-50 p-4 rounded-md">
                          <p className="text-sm text-gray-600 mb-2">
                            Found {results.subdomain.total_found} subdomains
                          </p>
                          <div className="space-y-1">
                            {results.subdomain.subdomains?.slice(0, 10).map((subdomain: string, index: number) => (
                              <div key={index} className="text-sm font-mono bg-white p-2 rounded">
                                {subdomain}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Port Scan Results */}
                    {results.port && (
                      <div>
                        <h4 className="font-medium text-green-600 mb-2">Port Scan</h4>
                        <div className="bg-gray-50 p-4 rounded-md">
                          <p className="text-sm text-gray-600 mb-2">
                            Found {results.port.open_ports?.length || 0} open ports
                          </p>
                          <div className="space-y-1">
                            {results.port.open_ports?.map((port: number, index: number) => (
                              <div key={index} className="text-sm font-mono bg-white p-2 rounded">
                                Port {port}: {results.port.services?.[port] || 'unknown'}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* DNS Results */}
                    {results.dns && (
                      <div>
                        <h4 className="font-medium text-purple-600 mb-2">DNS Records</h4>
                        <div className="bg-gray-50 p-4 rounded-md">
                          <div className="space-y-1">
                            {results.dns.records?.map((record: string, index: number) => (
                              <div key={index} className="text-sm font-mono bg-white p-2 rounded">
                                {record}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Technology Stack Results */}
                    {results.techstack && (
                      <div>
                        <h4 className="font-medium text-orange-600 mb-2">Technology Stack</h4>
                        <div className="bg-gray-50 p-4 rounded-md space-y-3">
                          {results.techstack.cms && (
                            <div>
                              <span className="text-sm font-medium text-gray-700">CMS: </span>
                              <span className="text-sm text-gray-900">{results.techstack.cms}</span>
                            </div>
                          )}
                          {results.techstack.web_server && (
                            <div>
                              <span className="text-sm font-medium text-gray-700">Web Server: </span>
                              <span className="text-sm text-gray-900">{results.techstack.web_server}</span>
                            </div>
                          )}
                          {results.techstack.technologies?.length > 0 && (
                            <div>
                              <span className="text-sm font-medium text-gray-700">Technologies: </span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {results.techstack.technologies.map((tech: string, index: number) => (
                                  <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                                    {tech}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}