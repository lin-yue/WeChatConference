function checkLength(formValue, length){
        if(formValue.length > length)
        {
            return 0;
        }
        return 1;
    }

    function checkEmptyForText(formValue)
    {
        if(formValue == "")
        {
            return 0;
        }
        return 1;
    }

    function checkIsNum(formValue)
    {
        if(isNaN(Number(formValue)))
        {
            return 0;
        }
        return 1;
    }

    function checkIsPosiveNum(formValue)
    {
        tempt = Number(formValue);
        if(isNaN(tempt))
        {
            return 0;
        }
        if(tempt < 0)
        {
            return 0;
        }
        return 1;
    }

    function checkEmptyForSelectOrRadio(formValue)
    {
        if(formValue < 0)
        {
            return 0;
        }
        return 1;
    }


    function validateForm(formGroupId, helpMsgId, formValue, validatorList, restrictList, errMsgList)
    {
        var i =0;
        var successFlag = 1;
        for(i = 0; i < validatorList.length; i++)
        {
            if(validatorList[i](formValue, restrictList[i]) == 0)
            {
                $(helpMsgId).text(errMsgList[i]);
                $(formGroupId).addClass("has-error");
                $(formGroupId).removeClass("has-success");
                successFlag = 0;
            }
        }
        if(successFlag == 1)
        {
            $(formGroupId).addClass("has-success");
            $(formGroupId).removeClass("has-error");
            $(helpMsgId).text("");
        }
        return successFlag;
    }