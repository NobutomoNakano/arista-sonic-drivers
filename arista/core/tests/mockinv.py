
import datetime

from ...inventory.fan import Fan
from ...inventory.interrupt import Interrupt
from ...inventory.led import Led
from ...inventory.phy import Phy
from ...inventory.powercycle import PowerCycle
from ...inventory.psu import Psu
from ...inventory.reloadcause import ReloadCause
from ...inventory.reset import Reset
from ...inventory.slot import Slot
from ...inventory.temp import Temp
from ...inventory.watchdog import Watchdog
from ...inventory.xcvr import Xcvr

class MockFan(Fan):
   def __init__(self, fanId=1, name="fan1", speed=12345, direction='forward'):
      self.fanId = fanId
      self.name = name
      self.speed = speed
      self.direction = direction

   def getName(self):
      return self.name

   def getSpeed(self):
      return self.speed

   def setSpeed(self, speed):
      self.speed = speed

   def getDirection(self):
      return self.direction

   def __eq__(self, value):
      return isinstance(value, MockFan) and self.fanId == value.fanId

class MockPsu(Psu):
   def __init__(self, psuId=1, name="psu1", presence=True, status=True):
      self.psuId = psuId
      self.name = name
      self.presence = presence
      self.status = status

   def getName(self):
      return self.name

   def getPresence(self):
      return self.presence

   def getStatus(self):
      return self.status

   def __eq__(self, value):
      return isinstance(value, MockPsu) and self.psuId == value.psuId

class MockWatchdog(Watchdog):
   def __init__(self, started=True, remaining=100, timeout=300):
      self.started = started
      self.remaining = remaining
      self.timeout = timeout

   def arm(self, timeout):
      self.timeout = timeout

   def stop(self):
      self.started = False
      self.remaining = 0

   def status(self):
      return self.started

class MockPowerCycle(PowerCycle):
   def __init__(self, powered=True):
      self.powered = powered

   def powerCycle(self):
      self.powered = not self.powered

   def __eq__(self, value):
      return isinstance(value, MockPowerCycle) and self.powered == value.powered

class MockReloadCause(ReloadCause):
   def __init__(self, name='unknown', time=datetime.datetime.now()):
      self.name = name
      self.time = time

   def getTime(self):
      return self.time

   def getCause(self):
      return self.name

class MockInterrupt(Interrupt):
   def __init__(self, name='unknown', status=False):
      self.name = name
      self.status = status
      self.path = '/test/path'

   def set(self):
      self.status = True

   def clear(self):
      self.status = False

   def getFile(self):
      return self.path

class MockReset(Reset):
   def __init__(self, name='unknown', reset=False):
      self.name = name
      self.reset = reset

   def read(self):
      return self.reset

   def resetIn(self):
      self.reset = True

   def resetOut(self):
      self.reset = False

   def getName(self):
      return self.name

class MockPhy(Phy):
   def __init__(self, phyId=1, reset=False):
      self.phyId = phyId
      self.reset = reset

   def getReset(self):
      return self.reset

   def __eq__(self, value):
      return isinstance(value, MockPhy) and self.phyId == value.phyId

class MockLed(Led):
   def __init__(self, name='unknown', color='green', status=True):
      self.name = name
      self.color = color
      self.status = status

   def getColor(self):
      return self.color

   def setColor(self, color):
      self.color = color

   def getName(self):
      return self.name

   def isStatusLed(self):
      return self.status

   def __eq__(self, value):
      return isinstance(value, MockLed) and self.name == value.name

class MockSlot(Slot):
   def __init__(self, name='unknown', present=True):
      self.name = name
      self.present = present

   def getPresence(self):
      return self.present

   def __eq__(self, value):
      return isinstance(value, MockSlot) and self.name == value.name

class MockXcvr(Xcvr):
   def __init__(self, portId=0, xcvrType=Xcvr.QSFP, name="unknown",
                presence=True, lpMode=False, intr=None, reset=None):
      self.portId = portId
      self.xcvrId = portId
      self.xcvrType = xcvrType
      self.name = name
      self.presence = presence
      self.lpMode = lpMode
      self.intr = intr
      self.reset = reset or MockReset('xcvr%d' % portId)

   def getType(self):
      return self.xcvrType

   def getName(self):
      return self.name

   def getPresence(self):
      return self.presence

   def getLowPowerMode(self):
      return self.lpMode

   def setLowPowerMode(self, value):
      self.lpMode = value

   def getInterruptLine(self):
      return self.intr

   def getReset(self):
      # TODO: introduce unsupported feature exceptions for inventory
      # if self.xcvrType == inventory.Xcvr.QSFP:
      #    raise FeatureNotSupported()
      return self.reset

class MockTemp(Temp):
   def __init__(self, diode=1, temperature=30, lowThreshold=10, highThreshold=50):
      self.diode = diode
      self.temperature = temperature
      self.lowThreshold = lowThreshold
      self.highThreshold = highThreshold

   def getTemperature(self):
      return self.temperature

   def getLowThreshold(self):
      return self.lowThreshold

   def setLowThreshold(self, value):
      self.lowThreshold = value * 1000

   def getHighThreshold(self):
      return self.highThreshold

   def setHighThreshold(self, value):
      self.highThreshold = value * 1000

   def __eq__(self, value):
      return isinstance(value, MockTemp) and self.diode == value.diode
