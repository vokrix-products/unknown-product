export interface Build {
  id: string
  service: string
  status: 'success' | 'failed' | 'pending'
  timestamp: string
}

export const builds: Build[] = [
  {
    id: '1',
    service: 'Railway',
    status: 'success',
    timestamp: '2024-01-01T00:00:00Z',
  },
]
