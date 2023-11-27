import cn from 'classnames'
import styles from './styles.module.css'
import { useContext } from 'react'
import { Button, LinkComponent } from '../index.js'
import { AuthContext } from '../../contexts'

const AccountMenu = ({ onSignOut }) => {
  const authContext = useContext(AuthContext)
  if (!authContext) {
    return <div className={styles.menu}>
      <LinkComponent
        className={styles.menuLink}
        href='/signin'
        title='Sign in'
      />
      <LinkComponent
        href='/signup'
        title='Create Account'
        className={styles.menuButton}
      />
    </div>
  }
  return <div className={styles.menu}>
    <LinkComponent
      className={styles.menuLink}
      href='/change-password'
      title='Change password'
    />
    <a
      className={styles.menuLink}
      onClick={onSignOut}
    >
      Sign out
    </a>
  </div>
}


export default AccountMenu
