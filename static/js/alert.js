function apiReturnParser(data) {
    console.log(data)
    if (data == 'false')
    {
        $.notify(data + ':  cannot connected with meshMixer, please restart meshMixer', { autoHide: true, className: 'error' });
        return false;
    }
    else
    {
        return true;
    }
}