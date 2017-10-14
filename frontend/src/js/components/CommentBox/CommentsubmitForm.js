import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { Button } from 'react-bootstrap';

const SimpleForm = props => {
  const { handleSubmit, pristine, reset, submitting, isSubmitting } = props
  console.log(isSubmitting);
  return (
      <form>
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
          <Button onClick={handleSubmit} disabled={pristine || submitting}>
            Submit
          </Button>
          <Button type="button" disabled={pristine || submitting} onClick={reset}>
            Clear Values
          </Button>
          { isSubmitting ? (<img src='static/images/loading.svg' height="50" width="50"/>):null}
        </div>
      </form>
  )
}

export default reduxForm({
  form: 'simple' // a unique identifier for this form
})(SimpleForm)