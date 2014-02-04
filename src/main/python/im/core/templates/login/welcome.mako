 <%inherit file="/core/crud/html/base.mako" />
 <form name="input" action="/test/auth/login/" method="post">
Username: <input type="text" name="username">
<input type="submit" value="Submit">

 <form class="form-horizontal" method="post" 
 action="/test/auth/login/" enctype="multipart/form-data">
                    <div class="row">
                    <div class="span12">
                    <div class="control-group">
                            <label class="control-label" for="username">Usuario</label>
                        <div class="controls">
                            <input
                                class=" "
                                type="text"
                                id="username"
                                name="username"
                                placeholder="Nombre de usuario"

                                >
                        </div>
                    </div>

                    <div class="control-group">
                            <label class="control-label" for="password">Clave</label>
                        <div class="controls">
                            <input
                                class=" "
                                type="password"
                                id="password"
                                name="password"


                                >
                        </div>
                    </div>
                    <div class="form-actions form-actions-no-background">
                    <input class="btn btn-primary" type="submit" name="submit" value="submit" />

                    </div>
                    </div>

                    </div>
                    </form>
