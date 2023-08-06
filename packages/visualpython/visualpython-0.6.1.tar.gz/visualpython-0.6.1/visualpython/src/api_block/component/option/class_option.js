define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../constData.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb,
              api, constData, baseComponent ) {

    const { RenderInputRequiredColor
            , GenerateClassInParamList } = api;

    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            
            , STR_COLON_SELECTED
            , STR_FOR
            , STR_EMPTY
            , STR_ONE_SPACE
            , STR_CHANGE_KEYUP_PASTE

            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED

            , STATE_className
            , STATE_parentClassName } = constData;

    const { MakeOptionContainer } = baseComponent;
            
    var InitClassBlockOption = function(thisBlock, optionPageSelector) {
        var uuid = thisBlock.getUUID();

        /**
         * @event_function
         * Class 이름 변경 이벤트 함수
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-class-name-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-class-name-${uuid}`, function(event) {
            RenderInputRequiredColor(this);
            thisBlock.setState({
                className: $(this).val()
            });
   
            $(`.vp-block-header-class-name-${thisBlock.getUUID()}`).html($(this).val());
            event.stopPropagation();
        });

        /**
         * @event_function
         * parent class 상속 값 입력 이벤트 함수
         */ 
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-param-0-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-param-0-${uuid}`, function(event) {

            thisBlock.setState({
                parentClassName: $(this).val()
            });
            var classInParamStr = GenerateClassInParamList(thisBlock);
            thisBlock.writeCode(classInParamStr);
            event.stopPropagation();
        });

        var RenderOptionPageName = function(thisBlock, name, blockCodeLineType) {
            var classStr = STR_EMPTY;
            var idStr = STR_EMPTY;
            var inputStyleStr = STR_EMPTY;
            var resetButton = null;
            var blockCodeName = thisBlock.getBlockName();
            var uuid = thisBlock.getUUID();
    
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS) {
                idStr = `vp_apiblockClassOptionName${uuid}`;
                classStr = `vp-apiblock-input-class-name-${uuid}`;
                blockCodeName = 'Name';
                inputStyleStr = 'width: 82%';
                /** state className에 문자열이 1개도 없을 때 */
                var classNameState = thisBlock.getState(STATE_className);
                if (classNameState == STR_EMPTY) {
                    classStr += STR_ONE_SPACE;
                    classStr += VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED;
                }
    
            } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
                idStr = `vp_apiblockDefOptionName${uuid}`;
                classStr = `vp-apiblock-input-def-name-${uuid}`;
                blockCodeName = 'Name';
                inputStyleStr = 'width: 82%';
                /** state defName에 문자열이 1개도 없을 때 */
                var defNameState = thisBlock.getState(STATE_defName);
                if (defNameState == STR_EMPTY) {
                   classStr += STR_ONE_SPACE;
                   classStr += VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED;
                }
    
            } 
           
            var nameDom = $(`<div class='vp-apiblock-blockoption-block 
                                         vp-apiblock-style-flex-row-between' 
                                   style='position:relative;'>
                               <span class='vp-block-optiontab-name 
                                            vp-apiblock-style-flex-column-center'>
                                   ${blockCodeName}
                               </span>
                               <input id='${idStr}'
                                      class='vp-apiblock-blockoption-input ${classStr}'
                                      style='${inputStyleStr}' 
                                      value="${name}"
                                      placeholder='input code line' ></input>   
                                                                                
                           </div>`);
                           
           if (resetButton !== null) {
               $(nameDom).append(resetButton);
           }
           return nameDom;
        }

        var RenderClassParentDom = function(thisBlock) {
            var uuid = thisBlock.getUUID();
            var parentClassName = thisBlock.getState(STATE_parentClassName);
     
            var name = 'Inheritance';
            var classStr = `vp-apiblock-input-param-${0}-${uuid}`;
            var inputStyleStr = 'width:66%;';
     
     
            var nameDom = $(`<div class='vp-block-blockoption 
                                            vp-apiblock-blockoption-block 
                                            vp-apiblock-blockoption-inner 
                                            vp-apiblock-style-flex-row-between' 
                                    style='position:relative;'>
                                    <span class='vp-block-optiontab-name 
                                                 vp-apiblock-style-flex-column-center'>${name}</span>
                                    <input class='vp-apiblock-blockoption-input 
                                                  ${classStr}'
                                        style='${inputStyleStr}' 
                                        value="${parentClassName}"
                                        placeholder='input parent class' ></input>   
                                                                                    
                                    </div>`);
            return nameDom;
        }

        /** 
         * @event_function
         * Class option 렌더링 
         */
        var renderThisComponent = function() {
            var classBlockOption = MakeOptionContainer(thisBlock);
            /** class name */
   
            var classNameState = thisBlock.getState(STATE_className);                                
            var classNameDom = RenderOptionPageName(thisBlock, classNameState, BLOCK_CODELINE_TYPE.CLASS);
            var classParentDom = RenderClassParentDom(thisBlock);
            classBlockOption.append(classNameDom);
            classBlockOption.append(classParentDom);

            /** */
            /** option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(classBlockOption);

            return classBlockOption;
        }
        
        return renderThisComponent();
    }

    return InitClassBlockOption;
});