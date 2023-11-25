import bpy


def get_selected_objects(context, ob_types=None):
    selected = []
    for ob in context.view_layer.objects:
        if not ob.select_get() or ob.hide_get() or ob.hide_viewport:
            continue
        if (ob_types is not None) and (ob.type not in ob_types):
            continue
        selected.append(ob)
    return selected

def get_armatures_actions_names(ob, include_nla):
    actions_names = set()
    if ob.animation_data is not None:
        if ob.animation_data.action is not None:
            actions_names.add(ob.animation_data.action.name)
        if include_nla:
            for nla_track in ob.animation_data.nla_tracks:
                for s in nla_track.strips:
                    if s.action is not None:
                        actions_names.add(s.action.name)
    return actions_names

def get_actions(actions_names):
    actions = []
    for an in actions_names:
        acc = bpy.data.actions.get(an, None)
        if acc is not None:
            actions.append(acc)
    return actions

def is_scaled(ob):
    for s in ob.scale:
        if abs(s-1) > 1e-6:
            return True
    return False

def topmost_parent(ob):
    act = ob
    while act.parent is not None:
        act = act.parent
    return act

def parenting_order_objects(obs):
    obs_names = set([ob.name for ob in obs])

    topmost_parents = {}
    for ob in obs:
        tp = topmost_parent(ob)
        topmost_parents[tp.name] = tp

    ordered_obs = []
    for ob in topmost_parents.values():
        acts = [ob]
        while len(acts) > 0:
            next_acts = []
            for act in acts:
                if act.name in obs_names:
                    ordered_obs.append(act)
                next_acts.extend([e for e in act.children])
            acts = next_acts

    return ordered_obs

def get_tuple_str(t, decimals):
    assert(len(t) > 0)
    t_str = "("
    for e in t[:-1]:
        t_str += " {:.{}f},".format(e, decimals)
    t_str += " {:.{}f} )".format(t[-1], decimals)
    return t_str

def adjust_constraints(ob, ob_scale):
    return

def scale_objects(obs, include_nla, silent=False):
    ordered_obs = parenting_order_objects(obs)

    scaled_armatures_names = {}
    already_scaled_acc_names = set()

    scaled_others_names = {}

    for ob in ordered_obs:
        if not is_scaled(ob):
            continue

        ob_scale = tuple(ob.scale)

        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        if ob.type != 'ARMATURE':
            scaled_others_names[ob.name] = ob_scale
            continue
        else:
            scaled_armatures_names[ob.name] = (ob_scale, set())
            ob_scaled_action_names = scaled_armatures_names[ob.name][1]

            ob_actions_names = get_armatures_actions_names(ob, include_nla)
            ob_actions_names = [n for n in ob_actions_names if n not in already_scaled_acc_names]
            ob_actions = get_actions(ob_actions_names)
            already_scaled_acc_names.update(ob_actions_names)
            del ob_actions_names

            for acc in ob_actions:
                for fcu in acc.fcurves:
                    if (not fcu.data_path.endswith('location')) or \
                       (fcu.data_path == 'location') or \
                       (len(fcu.keyframe_points) == 0):
                        continue

                    ob_scaled_action_names.add(acc.name)

                    scale = ob_scale[fcu.array_index]
                    for kfp in fcu.keyframe_points:
                        kfp.co[1] *= scale
                        kfp.handle_left[1] *= scale
                        kfp.handle_right[1] *= scale

            adjust_constraints(ob, ob_scale)

    n_armatures = len(scaled_armatures_names)
    n_others = len(scaled_others_names)

    if not silent:
        if n_armatures > 0:
            print("\n- Scaled armatures:")
            for ob_name, t in scaled_armatures_names.items():
                scale_str = get_tuple_str(t[0], decimals=5)
                if len(t[1]) == 0:
                    print("  \"{}\" (scale = {}; no actions).".format( ob_name, scale_str ) )
                else:
                    print("  \"{}\" (scale = {}; {} actions):".format( ob_name, scale_str, len(t[1]) ) )
                    for acc_name in t[1]:
                        print("    \"{}\"".format(acc_name))
                print()
        if n_others > 0:
            print("\n- Scaled non-armature objects:")
            for ob_name, scale in scaled_others_names.items():
                scale_str = get_tuple_str(scale, decimals=5)
                print( "  \"{}\" (scale = {})".format(ob_name, scale_str) )
            print()

    return n_armatures, n_others
