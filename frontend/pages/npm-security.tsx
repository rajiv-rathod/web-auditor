import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'
import toast from 'react-hot-toast'
import { npmApi } from '../lib/api'
import { 
  ShieldCheckIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  ClockIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'

interface AuditResult {
  status: string
  audit_results: any
  vulnerabilities_found: number
  summary: any
}

interface DependencyResult {
  status: string
  checked_packages: number
  results: any[]
}

interface LicenseResult {
  status: string
  total_packages: number
  risk_summary: {
    high: number
    medium: number
    low: number
    unknown: number
  }
  license_details: any[]
}

interface OutdatedResult {
  status: string
  outdated_count: number
  outdated_packages: any[]
}

export default function NPMSecurity() {
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('audit')
  const [packageJson, setPackageJson] = useState('')
  const [dependencies, setDependencies] = useState('')
  const [packageName, setPackageName] = useState('')
  
  // Results states
  const [auditResults, setAuditResults] = useState<AuditResult | null>(null)
  const [dependencyResults, setDependencyResults] = useState<DependencyResult | null>(null)
  const [licenseResults, setLicenseResults] = useState<LicenseResult | null>(null)
  const [outdatedResults, setOutdatedResults] = useState<OutdatedResult | null>(null)
  const [packageInfo, setPackageInfo] = useState<any>(null)

  const handleNpmAudit = async () => {
    if (!packageJson.trim()) {
      toast.error('Please provide package.json content')
      return
    }

    setLoading(true)
    try {
      const response = await npmApi.auditPackageJson(packageJson)
      setAuditResults(response.data)
      toast.success('NPM audit completed successfully!')
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'NPM audit failed'
      const displayMessage = typeof errorMessage === 'string' ? errorMessage : 
                             Array.isArray(errorMessage) ? errorMessage.map(e => e.msg || e).join(', ') :
                             'NPM audit failed'
      toast.error(displayMessage)
      console.error('NPM audit error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDependencyCheck = async () => {
    if (!dependencies.trim()) {
      toast.error('Please provide dependencies to check')
      return
    }

    const depList = dependencies.split('\n').map(dep => dep.trim()).filter(dep => dep)
    
    setLoading(true)
    try {
      const response = await npmApi.checkDependencies(depList)
      setDependencyResults(response.data)
      toast.success('Dependency check completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Dependency check failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLicenseScan = async () => {
    if (!packageJson.trim()) {
      toast.error('Please provide package.json content')
      return
    }

    setLoading(true)
    try {
      const response = await npmApi.scanLicenses(packageJson)
      setLicenseResults(response.data)
      toast.success('License scan completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'License scan failed')
    } finally {
      setLoading(false)
    }
  }

  const handleOutdatedCheck = async () => {
    if (!packageJson.trim()) {
      toast.error('Please provide package.json content')
      return
    }

    setLoading(true)
    try {
      const response = await npmApi.checkOutdatedPackages(packageJson)
      setOutdatedResults(response.data)
      toast.success('Outdated packages check completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Outdated packages check failed')
    } finally {
      setLoading(false)
    }
  }

  const handlePackageInfo = async () => {
    if (!packageName.trim()) {
      toast.error('Please provide a package name')
      return
    }

    setLoading(true)
    try {
      const response = await npmApi.getPackageInfo(packageName)
      setPackageInfo(response.data)
      toast.success('Package information retrieved!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to get package info')
    } finally {
      setLoading(false)
    }
  }

  const renderVulnerabilityBadge = (severity: string) => {
    const colors = {
      critical: 'bg-red-100 text-red-800',
      high: 'bg-orange-100 text-orange-800',
      moderate: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800',
      info: 'bg-blue-100 text-blue-800'
    }
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[severity as keyof typeof colors] || colors.info}`}>
        {severity}
      </span>
    )
  }

  const renderLicenseRisk = (risk: string) => {
    const colors = {
      high: 'text-red-600',
      medium: 'text-yellow-600',
      low: 'text-green-600',
      unknown: 'text-gray-600'
    }
    
    return (
      <span className={`font-semibold ${colors[risk as keyof typeof colors] || colors.unknown}`}>
        {risk.toUpperCase()}
      </span>
    )
  }

  return (
    <>
      <Head>
        <title>NPM Security - Web Auditor</title>
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
                <Link href="/" className="text-gray-700 hover:text-gray-900">Dashboard</Link>
                <Link href="/recon" className="text-gray-700 hover:text-gray-900">Reconnaissance</Link>
                <Link href="/vulnerability" className="text-gray-700 hover:text-gray-900">Vulnerability</Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Header */}
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <div className="flex items-center">
              <DocumentTextIcon className="h-8 w-8 text-green-600 mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">NPM Security Analysis</h1>
                <p className="text-gray-600">Comprehensive security analysis for Node.js packages and dependencies</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'audit', name: 'Security Audit', icon: ShieldCheckIcon },
                { id: 'dependencies', name: 'Dependency Check', icon: InformationCircleIcon },
                { id: 'licenses', name: 'License Scan', icon: DocumentTextIcon },
                { id: 'outdated', name: 'Outdated Packages', icon: ClockIcon },
                { id: 'info', name: 'Package Info', icon: ExclamationTriangleIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
                >
                  <tab.icon className="h-5 w-5 mr-2" />
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Input Section */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {activeTab === 'audit' && 'NPM Security Audit'}
                  {activeTab === 'dependencies' && 'Dependency Check'}
                  {activeTab === 'licenses' && 'License Compliance'}
                  {activeTab === 'outdated' && 'Outdated Packages'}
                  {activeTab === 'info' && 'Package Information'}
                </h3>

                {(activeTab === 'audit' || activeTab === 'licenses' || activeTab === 'outdated') && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Package.json Content
                      </label>
                      <textarea
                        value={packageJson}
                        onChange={(e) => setPackageJson(e.target.value)}
                        rows={12}
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                        placeholder={`{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}`}
                      />
                    </div>
                    <button
                      onClick={
                        activeTab === 'audit' ? handleNpmAudit :
                        activeTab === 'licenses' ? handleLicenseScan :
                        handleOutdatedCheck
                      }
                      disabled={loading}
                      className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                    >
                      {loading ? 'Analyzing...' : 
                        activeTab === 'audit' ? 'Run Security Audit' :
                        activeTab === 'licenses' ? 'Scan Licenses' :
                        'Check Outdated Packages'
                      }
                    </button>
                  </div>
                )}

                {activeTab === 'dependencies' && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Dependencies (one per line)
                      </label>
                      <textarea
                        value={dependencies}
                        onChange={(e) => setDependencies(e.target.value)}
                        rows={8}
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                        placeholder={`express
lodash
react
vue
axios`}
                      />
                    </div>
                    <button
                      onClick={handleDependencyCheck}
                      disabled={loading}
                      className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                    >
                      {loading ? 'Checking...' : 'Check Dependencies'}
                    </button>
                  </div>
                )}

                {activeTab === 'info' && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Package Name
                      </label>
                      <input
                        type="text"
                        value={packageName}
                        onChange={(e) => setPackageName(e.target.value)}
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                        placeholder="express"
                      />
                    </div>
                    <button
                      onClick={handlePackageInfo}
                      disabled={loading}
                      className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                    >
                      {loading ? 'Getting Info...' : 'Get Package Info'}
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Results Section */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>

                {/* NPM Audit Results */}
                {activeTab === 'audit' && auditResults && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-red-50 p-4 rounded-lg">
                        <div className="text-2xl font-bold text-red-600">{auditResults.vulnerabilities_found}</div>
                        <div className="text-sm text-red-800">Total Vulnerabilities</div>
                      </div>
                      <div className="bg-yellow-50 p-4 rounded-lg">
                        <div className="text-2xl font-bold text-yellow-600">
                          {auditResults.summary?.vulnerabilities?.moderate || 0}
                        </div>
                        <div className="text-sm text-yellow-800">Moderate</div>
                      </div>
                      <div className="bg-red-50 p-4 rounded-lg">
                        <div className="text-2xl font-bold text-red-600">
                          {auditResults.summary?.vulnerabilities?.high || 0}
                        </div>
                        <div className="text-sm text-red-800">High/Critical</div>
                      </div>
                    </div>

                    {auditResults.audit_results?.vulnerabilities && (
                      <div className="mt-6">
                        <h4 className="text-md font-medium text-gray-900 mb-3">Vulnerability Details</h4>
                        <div className="space-y-3">
                          {Object.entries(auditResults.audit_results.vulnerabilities).map(([id, vuln]: [string, any]) => (
                            <div key={id} className="border rounded-lg p-4">
                              <div className="flex justify-between items-start mb-2">
                                <h5 className="font-medium text-gray-900">{vuln.title}</h5>
                                {renderVulnerabilityBadge(vuln.severity)}
                              </div>
                              <p className="text-sm text-gray-600 mb-2">{vuln.overview}</p>
                              <div className="text-xs text-gray-500">
                                <span>Module: {vuln.module_name}</span>
                                {vuln.patched_versions && (
                                  <span className="ml-4">Patched: {vuln.patched_versions}</span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Dependency Check Results */}
                {activeTab === 'dependencies' && dependencyResults && (
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">{dependencyResults.checked_packages}</div>
                      <div className="text-sm text-blue-800">Packages Checked</div>
                    </div>

                    <div className="space-y-3">
                      {dependencyResults.results.map((result, index) => (
                        <div key={index} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start">
                            <div>
                              <h5 className="font-medium text-gray-900">{result.package}</h5>
                              {result.description && (
                                <p className="text-sm text-gray-600">{result.description}</p>
                              )}
                              {result.latest_version && (
                                <p className="text-xs text-gray-500">Latest: {result.latest_version}</p>
                              )}
                            </div>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              result.status === 'found' ? 'bg-green-100 text-green-800' :
                              result.status === 'not_found' ? 'bg-red-100 text-red-800' :
                              'bg-yellow-100 text-yellow-800'
                            }`}>
                              {result.status}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* License Results */}
                {activeTab === 'licenses' && licenseResults && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-red-50 p-4 rounded-lg text-center">
                        <div className="text-2xl font-bold text-red-600">{licenseResults.risk_summary.high}</div>
                        <div className="text-sm text-red-800">High Risk</div>
                      </div>
                      <div className="bg-yellow-50 p-4 rounded-lg text-center">
                        <div className="text-2xl font-bold text-yellow-600">{licenseResults.risk_summary.medium}</div>
                        <div className="text-sm text-yellow-800">Medium Risk</div>
                      </div>
                      <div className="bg-green-50 p-4 rounded-lg text-center">
                        <div className="text-2xl font-bold text-green-600">{licenseResults.risk_summary.low}</div>
                        <div className="text-sm text-green-800">Low Risk</div>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg text-center">
                        <div className="text-2xl font-bold text-gray-600">{licenseResults.risk_summary.unknown}</div>
                        <div className="text-sm text-gray-800">Unknown</div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      {licenseResults.license_details.map((license, index) => (
                        <div key={index} className="border rounded-lg p-4">
                          <div className="flex justify-between items-center">
                            <div>
                              <h5 className="font-medium text-gray-900">{license.package}</h5>
                              <p className="text-sm text-gray-600">License: {license.license}</p>
                            </div>
                            {renderLicenseRisk(license.risk_level)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Outdated Packages Results */}
                {activeTab === 'outdated' && outdatedResults && (
                  <div className="space-y-4">
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-yellow-600">{outdatedResults.outdated_count}</div>
                      <div className="text-sm text-yellow-800">Outdated Packages</div>
                    </div>

                    {outdatedResults.outdated_packages.length > 0 ? (
                      <div className="space-y-3">
                        {outdatedResults.outdated_packages.map((pkg, index) => (
                          <div key={index} className="border rounded-lg p-4">
                            <h5 className="font-medium text-gray-900">{pkg.package}</h5>
                            <div className="text-sm text-gray-600 mt-1">
                              <span>Current: {pkg.current}</span>
                              <span className="mx-2">→</span>
                              <span>Latest: {pkg.latest}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-green-600">All packages are up to date!</p>
                    )}
                  </div>
                )}

                {/* Package Info Results */}
                {activeTab === 'info' && packageInfo && (
                  <div className="space-y-4">
                    <div className="border rounded-lg p-4">
                      <h4 className="text-lg font-medium text-gray-900">{packageInfo.name}</h4>
                      <p className="text-gray-600 mt-1">{packageInfo.description}</p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                        <div>
                          <span className="text-sm font-medium text-gray-500">Version:</span>
                          <span className="ml-2 text-sm text-gray-900">{packageInfo.version}</span>
                        </div>
                        <div>
                          <span className="text-sm font-medium text-gray-500">License:</span>
                          <span className="ml-2 text-sm text-gray-900">{packageInfo.license}</span>
                        </div>
                        <div>
                          <span className="text-sm font-medium text-gray-500">Author:</span>
                          <span className="ml-2 text-sm text-gray-900">{packageInfo.author || 'N/A'}</span>
                        </div>
                        <div>
                          <span className="text-sm font-medium text-gray-500">Downloads:</span>
                          <span className="ml-2 text-sm text-gray-900">{packageInfo.downloads || 'N/A'}</span>
                        </div>
                      </div>

                      {packageInfo.homepage && (
                        <div className="mt-4">
                          <span className="text-sm font-medium text-gray-500">Homepage:</span>
                          <a href={packageInfo.homepage} target="_blank" rel="noopener noreferrer" className="ml-2 text-sm text-blue-600 hover:text-blue-800">
                            {packageInfo.homepage}
                          </a>
                        </div>
                      )}

                      {packageInfo.keywords && packageInfo.keywords.length > 0 && (
                        <div className="mt-4">
                          <span className="text-sm font-medium text-gray-500">Keywords:</span>
                          <div className="mt-1 flex flex-wrap gap-1">
                            {packageInfo.keywords.map((keyword: string, index: number) => (
                              <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                {keyword}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* No Results */}
                {!auditResults && !dependencyResults && !licenseResults && !outdatedResults && !packageInfo && (
                  <div className="text-center py-12">
                    <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No analysis results</h3>
                    <p className="mt-1 text-sm text-gray-500">
                      Run an analysis to see results here
                    </p>
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