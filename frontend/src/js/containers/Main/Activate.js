import React from "react";
import { connect } from 'react-redux';
import { Verification } from '../../actions/userActions'
import { actions as notifActions, Notifs } from 'redux-notifications';
const { notifSend, notifDismiss } = notifActions;
import { withRouter } from 'react-router';


const s ={
  'display': 'block',
  'width': '100%',
  'color': '#fff',
  'backgroundColor': '#d9534f',
  'borderColor': '#d43f3a',
  'padding': '10px 16px',
  'fontSize': '18px',
  'lineHeight': '1.3333333',
  'borderRadius': '0',
  'textAlign': 'center',
  'whiteSpace': 'nowrap',
  'verticalAlign': 'middle',
  'fontWeight': '400',
  'marginBottom': '0',
}
const s2 ={
  'display': 'block',
  'width': '100%',
  'color': '#fff',
  'backgroundColor': '#5cb85c',
  'borderColor': '#5cb85c',
  'padding': '10px 16px',
  'fontSize': '18px',
  'lineHeight': '1.3333333',
  'borderRadius': '0',
  'textAlign': 'center',
  'whiteSpace': 'nowrap',
  'verticalAlign': 'middle',
  'fontWeight': '400',
  'marginBottom': '0',
}

function FailNotf(props) {
  return (
      <div style={s} onClick={() => {
        if (props.onActionClick) {
          props.onActionClick(props.id);
        }
      }}>
        {props.message}
      </div>
  );
}

function SuccessNotf(props) {
  return (
      <div style={s2} onClick={() => {
        if (props.onActionClick) {
           props.onActionClick(props.id);
          }
        }}>
        {props.message}
      </div>
  );
}

@connect((store) => {
  return {
    discover: store.games.discover,
  }
})
class Activate extends React.Component {
  constructor(props) {
    super(props);
    this.state= {
      isSuccess:false
    };
    this.dismiss = this.dismiss.bind(this);
  }


  activatenotf() {
    this.props.dispatch(notifSend({
      message: 'You now has been activated Successfully, Click here and login in',
      kind: 'info',
      dismissAfter: 60000
    }));
  }

  failactivatenotf() {
    this.props.dispatch(notifSend({
      message: 'Fail to activate, Please Click here and try again.',
      kind: 'danger',
      dismissAfter: 60000,
    }));
  }

  dismiss(id) {
    this.props.dispatch(notifDismiss(id));
    this.props.history.push('/discover');
  }

  componentWillMount() {
    const key=this.props.match.params.key;
    Verification(key)
        .then((res)=>{
          console.log(res)
          this.activatenotf();
          this.setState({
            isSuccess:true,
          })
        })
        .catch((err)=>{
          console.log(err);
          this.failactivatenotf();
          this.setState({
            isSuccess:false,
          })
        });

  }


  render() {
    if(this.state.isSuccess){
      return (
          <div>
            <Notifs
                CustomComponent={SuccessNotf}
                onActionClick={id => this.dismiss(id)}
            />
          </div>
      )
    }
    return (
        <div>
          <Notifs
              CustomComponent={FailNotf}
              onActionClick={id => this.dismiss(id)}
          />
        </div>
    )
  }
}

const ActivateRouter = withRouter(Activate);
export default ActivateRouter;
