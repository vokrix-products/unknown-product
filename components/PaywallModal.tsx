import React from 'react'

interface PaywallModalProps {
  isOpen: boolean
  onClose: () => void
}

const PaywallModal: React.FC<PaywallModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg p-6 max-w-md">
        <h2 className="text-xl font-bold">Upgrade to Pro</h2>
        <p className="mt-2">Unlock all features for just $9/month.</p>
        <button onClick={onClose} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Close</button>
      </div>
    </div>
  )
}

export default PaywallModal
