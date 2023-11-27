import { Container, Input, Title, Main, Form, Button } from '../../components'
import styles from './styles.module.css'
import { useFormWithValidation } from '../../utils'
import { AuthContext } from '../../contexts'
import { Redirect } from 'react-router-dom'
import { useContext } from 'react'
import MetaTags from 'react-meta-tags'

const SignIn = ({ onSignIn }) => {
  const { values, handleChange, errors, isValid, resetForm } = useFormWithValidation()
  const authContext = useContext(AuthContext)

  return <Main>
    {authContext && <Redirect to='/recipes' />}
    <Container>
      <MetaTags>
        <title>Sign in</title>
        <meta name="description" content="Groccery Assistant - Sign in" />
        <meta property="og:title" content="Sign in" />
      </MetaTags>
      <Title title='Sign in' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          onSignIn(values)
        }}
      >
        <Input
          required
          label='Email'
          name='email'
          onChange={handleChange}
        />
        <Input
          required
          label='Password'
          type='password'
          name='password'
          onChange={handleChange}
        />
        <Button
          modifier='style_dark-blue'
          disabled={!isValid}
          type='submit'
          className={styles.button}
        >
          Sign in
        </Button>
      </Form>
    </Container>
  </Main>
}

export default SignIn
