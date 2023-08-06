define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/common/vpMakeDom'

    , '../../api.js'    
    , '../../constData.js'
    
], function ( $, vpCommon, vpConst, sb, 
              vpFuncJS, libPandas, vpMakeDom,
              api, constData ) {

    const { VP_CLASS_STYLE_FLEX_COLUMN_CENTER } = constData;

    var MakeOptionButton_type2 = function(id, className, title ) {
        var sbOptionButtonType2 = new sb.StringBuilder();
        
        sbOptionButtonType2.appendFormatLine("<div id='{0}' class='{1}'>", id, className);
        sbOptionButtonType2.appendFormatLine("<button class='{0}'>" , 'vp-block-long-plus-button');
        sbOptionButtonType2.appendFormatLine("{0}", title);                                                    
        sbOptionButtonType2.appendLine("</button>"); 
        sbOptionButtonType2.appendLine("</div>");

        return sbOptionButtonType2.toString();
    }
    return MakeOptionButton_type2;
});