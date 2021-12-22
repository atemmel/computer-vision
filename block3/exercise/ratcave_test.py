#!/usr/bin/env python
import pyglet
import ratcave as rc
from pyglet.window import key

x = 0

vert_shader = """
#version 120

attribute vec3 vertexPosition;
attribute vec3 normalPosition;
uniform mat4 model_matrix, normal_matrix;
uniform mat4 view_matrix = mat4(1.0);
uniform mat4 projection_matrix = mat4(
    vec4(1.38564062,  0.,  0.,  0.),
    vec4(0.,  1.73205078,  0.,  0.),
    vec4(0., 0., -1.01680672, -1. ),
    vec4(0., 0., -0.20168068, 0.)
);

varying vec4 vVertex;
varying vec3 normal;

void main()
{
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertexPosition, 1.0);
    vVertex = model_matrix * vec4(vertexPosition, 1.0);
    normal = normalize(normal_matrix * vec4(normalPosition, 1.0)).xyz;
}
"""

frag_shader = """
#version 120
uniform vec3 camera_position, light_position;
uniform vec3 diffuse, ambient;

varying vec3 normal;
varying vec4 vVertex;

vec4 doLambert(vec3 vertex, vec3 normal, vec3 light_position, vec3 camera_position, vec3 ambient, vec3 diffuse) {
    vec4 color = vec4(ambient, 1.);
    vec3 light_direction = normalize(light_position - vertex);

    vec3 reflectionVector = reflect(light_direction, normalize(normal));
    float cosAngle = max(0.0, -dot(normalize(camera_position - vertex), reflectionVector));

    ambient = vec3(0.2, 0.2, 0.2);
    vec3 i = ambient + (cosAngle * vec3(0.5, 0.5, 0.5));
    //vec3 i = ambient;

    return vec4(i, 1);
}

void main()
{
    gl_FragColor = doLambert(vVertex.xyz, normal, light_position, camera_position, ambient, diffuse);

}
"""

shader = rc.Shader(vert=vert_shader, frag=frag_shader)

window = pyglet.window.Window()
pyglet.clock.schedule(lambda dt: dt)

file = rc.resources.obj_primitives
monkey = rc.WavefrontReader(file).get_mesh("Monkey")
monkey.position.xyz = 0, 0, -2

scene = rc.Scene(meshes=[monkey])

@window.event
def on_key_press(symbol, _):
    global x
    if symbol == key.RIGHT:
       x += 0.05
    elif symbol == key.LEFT:
       x -= 0.05
    scene.camera.position.xyz = x, 0, 0

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()
