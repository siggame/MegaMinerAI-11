#include "animations.h"
#include "${lowercase(gameName)}.h"

namespace visualizer
{
  void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* /*game*/ )
  {
  }

  void DrawSomething::animate( const float& /*t*/, AnimData * /*d*/, IGame* game )
  {
    // Set the color to red
    game->renderer->setColor( Color( 1, 0, 0, 1 ) );
    // Draw a 2x2 rectangle at (1,1), with the top left corner of the screen being the origin 
    game->renderer->drawQuad( 1, 1, 2, 2 );
  }

}
