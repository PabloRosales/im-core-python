<%inherit file="/core/view.mako"/>

<div class="container">

    <div id="login" class="row">
        <div class="span12">

          % if failed_attempt:
              <div class="alert alert-warning">
                <strong>${t('WRONG_USERNAME_OR_PASSWORD')}</a>.
              </div>
          % endif

            <form class="form-horizontal" action='' method="POST">
                <fieldset>
                  <div id="legend">
                    <legend class="">${t('LOGIN')}</legend>
                  </div>    
                  <div class="control-group">
                    <!-- Username -->
                    <label class="control-label"  for="username">${t('USERNAME')}</label>
                    <div class="controls">
                      <input type="text" id="username" name="username" placeholder="" class="input-xlarge">
                    </div>
                  </div>

                  <div class="control-group">
                    <!-- Password-->
                    <label class="control-label" for="password">${t('PASSWORD')}</label>
                    <div class="controls">
                      <input type="password" id="password" name="password" placeholder="" class="input-xlarge">
                      <input class=" " type="hidden" id="return_url" name="return_url" value="${BASE}" />
                    </div>
                  </div>


                  <div class="control-group">
                    <!-- Button -->
                    <div class="controls">
                      <button class="btn btn-success">${t('LOGIN')}</button>
                    </div>
                  </div>
                </fieldset>
            </form>                
        </div> 
    </div> 

</div> 
