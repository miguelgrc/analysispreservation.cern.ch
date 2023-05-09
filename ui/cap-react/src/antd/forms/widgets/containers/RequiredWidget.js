import { connect } from "react-redux";

import { updateRequired } from "../../../../actions/schemaWizard";
import RequiredWidget from "../RequiredWidget";

const mapStateToProps = state => ({
  path: state.schemaWizard.get("field"),
  fullSchema: state.schemaWizard.getIn(["current", "schema"]),
});

const mapDispatchToProps = dispatch => ({
  updateRequired: (path, fieldName, isRequired) =>
    dispatch(updateRequired(path, fieldName, isRequired)),
});

export default connect(mapStateToProps, mapDispatchToProps)(RequiredWidget);
