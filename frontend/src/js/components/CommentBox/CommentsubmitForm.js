import React from 'react'
import { Field, reduxForm } from 'redux-form'

const SimpleForm = props => {
  const { handleSubmit, pristine, reset, submitting } = props
  return (
      <form onSubmit={handleSubmit}>
        <div>
          <label>Rate</label>
          <div>
            <label>
              <Field
                  name="rate"
                  component="input"
                  type="radio"
                  value="true"
              />{' '}
              Recommend
            </label>
            <label className='rate-btn'>
              <Field
                  name="rate"
                  component="input"
                  type="radio"
                  value='false'
              />{' '}
              UnRecommend
            </label>
          </div>
        </div>
        <div>
          <label>Review</label>
          <div>
            <Field name="Review" component="textarea" className='review-input' />
          </div>
        </div>
        <div>
          <button type="submit" disabled={pristine || submitting}>
            Submit
          </button>
          <button type="button" disabled={pristine || submitting} onClick={reset}>
            Clear Values
          </button>
        </div>
      </form>
  )
}

export default reduxForm({
  form: 'simple' // a unique identifier for this form
})(SimpleForm)