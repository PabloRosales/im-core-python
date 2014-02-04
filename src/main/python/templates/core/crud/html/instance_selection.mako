<ul class="instance-selection">
    % for instance, config in instances.iteritems():
        <li>
            <h3>
                <i class="icon-arrow-right"></i>
                <a href="${current_url(strip_querystring=True, instance=instance)}">${config['name']}</a>
            </h3>
        </li>
    % endfor
</ul>
