// eslint-disable-next-line no-unused-vars
import React from 'react'
//import LidarPatientMonitor from './components/LidarPatientMonitor'
import PatientDashboard from './components/patientDashboard'
import ErrorBoundary from './components/ErrorBoundry'


function App() {
  return (
    <div className="App">
      <ErrorBoundary>
        <PatientDashboard />
      </ErrorBoundary>
    </div>
  )
}

export default App