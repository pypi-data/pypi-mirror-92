define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpTableLayoutVerticalSimple'

    , 'codemirror/lib/codemirror'
    , 'codemirror/mode/python/python'
    , 'notebook/js/codemirror-ipython'
    , 'codemirror/addon/display/placeholder'

    , '../../api.js'    
    , '../../constData.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpTableLayoutVerticalSimple, codemirror, codemirrorMode, 
              codemirrorIpython, codemirrorAddon,

              api,constData, baseComponent ) {
                  
    const {  STATE_codeLine
            , NUM_MAX_ITERATION
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;

    const { MakeOptionContainer } = baseComponent;

    var InitNodeBlockOption = function(thisBlock, optionPageSelector) {
        var blockContainerThis = thisBlock.getBlockContainerThis();

        /** node option 렌더링 */
        var renderThisComponent = function() {
            var nodeBlockOption = MakeOptionContainer(thisBlock);
            thisBlock.writeCode(thisBlock.getState(STATE_codeLine));

            var codeLineList = blockContainerThis.previewCode(thisBlock);

            var textareaDom = document.createElement('textarea');
            $(textareaDom).val(codeLineList);
            $(textareaDom).attr('id','vp_userCode');
            $(textareaDom).attr('name','code');
            $(textareaDom).attr('style','display: none');
       
            // $(nodeBlockOption).empty();
            nodeBlockOption.append(textareaDom);

            var codemirrorCode = codemirror.fromTextArea(textareaDom, {
                mode: {
                    name: 'python',
                    version: 3,
                    singleLineStringErrors: false
                },  // text-cell(markdown cell) set to 'htmlmixed'
                indentUnit: 4,
                matchBrackets: true,
                readOnly:true,
                autoRefresh: true,
                lineWrapping: false, // text-cell(markdown cell) set to true
                indentWithTabs: true,
                theme: "ipython",
                extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"}
            });
  
            $(optionPageSelector).append(nodeBlockOption);
            codemirrorCode.setValue($(textareaDom).val());

            return nodeBlockOption;
        }
        return renderThisComponent();
    }       
    return InitNodeBlockOption;
});