// Auto-generated
import { TriangleAlert, CircleCheckBig, Clock, Archive } from 'lucide-react'
import type { ComponentType } from 'react'

export interface StatusType {
  label: string
  value: string
  icon: ComponentType<{ className?: string }>
  severity: string
}

export const statuses = [
  {
    label: "Above Threshold",
    value: "above_threshold:critical",
    icon: TriangleAlert,
    severity: "critical",
  },
  {
    label: "Within Threshold",
    value: "within_threshold:good",
    icon: CircleCheckBig,
    severity: "good",
  },
  {
    label: "Expires Soon",
    value: "expires_soon:warning",
    icon: Clock,
    severity: "warning",
  },
  {
    label: "Archived",
    value: "archived:neutral",
    icon: Archive,
    severity: "neutral",
  },
]

export const severityToBadgeVariant: Record<string, 'default' | 'success' | 'warning' | 'destructive'> = {
  critical: 'destructive',
  good: 'success',
  warning: 'warning',
  neutral: 'default',
}
