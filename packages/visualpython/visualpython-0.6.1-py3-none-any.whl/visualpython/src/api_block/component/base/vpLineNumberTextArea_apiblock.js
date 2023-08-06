/** src/common에 있는 vpLineNumberTextArea을 api block에 맞게 커스텀 */define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'

    , '../../api.js'    
    , '../../constData.js'
    
], function ( $, vpCommon, vpConst, sb, vpLineNumberTextArea,
              api, constData ) {
                  
    var vpLineNumberTextArea_apiblock = function(id, codeState, styleObj) {
        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea( id, 
                                                                                codeState);     
                          
        lineNumberTextArea.setHeight('250px');        
        var lineNumberTextAreaStr = lineNumberTextArea.toTagString();
        return lineNumberTextAreaStr;
    }

    return vpLineNumberTextArea_apiblock;
});