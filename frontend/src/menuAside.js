import {
  mdiAccountMultiple,
  mdiClockEdit,
  mdiCog,
} from '@mdi/js'

export default [
  {
    to: '/workers',
    label: 'Workers',
    icon: mdiAccountMultiple,
  },
  {
    to: '/shifts',
    label: 'Shifts',
    icon: mdiClockEdit,
  },
  {
    to: '/settings',
    label: 'Settings',
    icon: mdiCog,
  },
]
