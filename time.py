import { useState, useEffect } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "/components/ui/select"
import { Clock } from "lucide-react"

// List of time zones with their display names and UTC offsets
const TIME_ZONES = [
  { id: 'UTC', name: 'UTC', offset: 0 },
  { id: 'EST', name: 'Eastern Time (EST)', offset: -5 },
  { id: 'PST', name: 'Pacific Time (PST)', offset: -8 },
  { id: 'CET', name: 'Central European Time (CET)', offset: 1 },
  { id: 'GMT', name: 'Greenwich Mean Time (GMT)', offset: 0 },
  { id: 'IST', name: 'Indian Standard Time (IST)', offset: 5.5 },
  { id: 'JST', name: 'Japan Standard Time (JST)', offset: 9 },
  { id: 'AEST', name: 'Australian Eastern Time (AEST)', offset: 10 },
  { id: 'BRT', name: 'Brasília Time (BRT)', offset: -3 },
  { id: 'CST', name: 'China Standard Time (CST)', offset: 8 },
]

export default function TimeZoneDashboard() {
  const [displayedTimeZones, setDisplayedTimeZones] = useState(TIME_ZONES.slice(0, 6))
  const [currentTimes, setCurrentTimes] = useState<Record<string, string>>({})
  const [selectedTimeZone, setSelectedTimeZone] = useState('')

  // Format time with AM/PM
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
  }

  // Calculate current time for each displayed time zone
  const updateTimes = () => {
    const now = new Date()
    const newTimes: Record<string, string> = {}

    displayedTimeZones.forEach(tz => {
      const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000)
      const tzTime = new Date(utcTime + (3600000 * tz.offset))
      newTimes[tz.id] = formatTime(tzTime)
    })

    setCurrentTimes(newTimes)
  }

  // Update times every second
  useEffect(() => {
    updateTimes()
    const interval = setInterval(updateTimes, 1000)
    return () => clearInterval(interval)
  }, [displayedTimeZones])

  // Add a new time zone to the display
  const addTimeZone = () => {
    if (!selectedTimeZone) return
    
    const tzToAdd = TIME_ZONES.find(tz => tz.id === selectedTimeZone)
    if (!tzToAdd || displayedTimeZones.some(tz => tz.id === selectedTimeZone)) return
    
    setDisplayedTimeZones([...displayedTimeZones, tzToAdd])
    setSelectedTimeZone('')
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Time Zone Dashboard</h1>
        
        <div className="mb-8 flex flex-col md:flex-row gap-4">
          <Select value={selectedTimeZone} onValueChange={setSelectedTimeZone}>
            <SelectTrigger className="w-full md:w-64">
              <SelectValue placeholder="Select a time zone" />
            </SelectTrigger>
            <SelectContent>
              {TIME_ZONES.map(tz => (
                <SelectItem 
                  key={tz.id} 
                  value={tz.id}
                  disabled={displayedTimeZones.some(dtz => dtz.id === tz.id)}
                >
                  {tz.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button onClick={addTimeZone} disabled={!selectedTimeZone}>
            Add Time Zone
          </Button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayedTimeZones.map(tz => (
            <Card key={tz.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-gray-600" />
                  <span>{tz.name}</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-mono font-bold">
                  {currentTimes[tz.id] || 'Loading...'}
                </div>
                <div className="text-sm text-gray-500 mt-2">
                  UTC{tz.offset >= 0 ? '+' : ''}{tz.offset}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
