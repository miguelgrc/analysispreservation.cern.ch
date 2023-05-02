import { connect } from "react-redux";
import RequiredWidget from "../RequiredWidget";
import { updateRequired } from "../../../../actions/schemaWizard";

const mapStateToProps = state => ({
  path: state.schemaWizard.get("field"),
});

const mapDispatchToProps = dispatch => ({
  updateRequired: (path, fieldName, isRequired) =>
    dispatch(updateRequired(path, fieldName, isRequired)),
});

export default connect(mapStateToProps, mapDispatchToProps)(RequiredWidget);
