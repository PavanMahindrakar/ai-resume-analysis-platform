/**
 * Keyboard accessibility utilities
 */

export const KEYBOARD_KEYS = {
  ENTER: 'Enter',
  SPACE: ' ',
  ESCAPE: 'Escape',
  TAB: 'Tab',
  ARROW_UP: 'ArrowUp',
  ARROW_DOWN: 'ArrowDown',
  ARROW_LEFT: 'ArrowLeft',
  ARROW_RIGHT: 'ArrowRight',
  HOME: 'Home',
  END: 'End',
} as const

/**
 * Check if a keyboard event is an activation key (Enter or Space)
 */
export function isActivationKey(event: React.KeyboardEvent): boolean {
  return event.key === KEYBOARD_KEYS.ENTER || event.key === KEYBOARD_KEYS.SPACE
}

/**
 * Handle keyboard activation (Enter/Space) on clickable elements
 */
export function handleKeyboardActivation(
  event: React.KeyboardEvent,
  callback: () => void
) {
  if (isActivationKey(event)) {
    event.preventDefault()
    callback()
  }
}

/**
 * Check if event target is a form element
 */
export function isFormElement(element: HTMLElement): boolean {
  const formElements = ['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON']
  return formElements.includes(element.tagName)
}
