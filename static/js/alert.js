function apiReturnParser(data) {
    console.log(data)
    if (data == 'false')
    {
        $.notify('Please wait, an operation is under way.', { autoHide: false, className: 'info' });
        return false;
    }
    else
    {
        return true;
    }
}