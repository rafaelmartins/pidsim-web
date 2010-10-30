var model = null;

function select_model(model) {
    $("#graph").html('');
    $.getJSON('model/' + model, function(data) {
        $('#model_id').html(data.model['id']);
        $('#model_img').attr('src', data.model['img']);
        if(data.model['form'] != null){
            $('#additional_form').html(data.model['form']);
        }
        else{
            $('#additional_form').html("{{ _('Sem parametros.') }}");
        }
        $('#selected_model').show();
        $('#what').val('1');
    });
}

$(document).ready(function() {
    $("#t_method").change(function(){
        if($(this).val() == "0"){
            $("#pid_parameters").show();
            $("#what").val('2');
            $("#what").attr("disabled", true);
        }
        else{
            $("#pid_parameters").hide();
            $("#what").val('1');
            $("#what").attr("disabled", false);
        }
    });
    $("#options").validate({
        onsubmit: true,
        onfocusout: false,
        onkeyup: false,
        onclick: false,
        submitHandler: function(form) {
            // Validation to save resources :P
            if(($("#total").val() / $("#sample").val()) > 5000){
                window.alert(
                    "{{ _('Erro: \\n\\nSeu gráfico teria mais de 5000 pontos.\\n') }}" + 
                    "{{ _('Por favor, diminua o Tempo Total ou aumente o Tempo de Amostragem.') }}"
                );
                return false;
            }
            // Wow, we have a model to plot! :D
            ts = Math.round(new Date().getTime() / 1000);
            img_url = 'plot/' + model + '?' + $("#options").serialize();
            $('#graph').html('<img src="' + img_url + '&uts=' + ts + '" />');
            return false;
        },
        showErrors: function(errorMap, errorList) {
            if(errorList.length > 0) {
                // Dammit!
                var aux = "{{ _('Erros:\\n\\n') }}";
                for(key in errorMap) {
                    aux += key + ": " + errorMap[key] + "\n";
                }
                window.alert(aux);
            }
        }
    });
});
